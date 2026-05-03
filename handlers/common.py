from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from knowledge_base import KnowledgeBase
from keyboards.applicant_kb import get_applicant_menu_inline
from keyboards.main_menu import get_main_menu_keyboard
from keyboards.student_kb import get_student_menu_inline
from keyboards.teacher_kb import get_teacher_menu_inline
from services.navigation import (
    get_common_menu_text,
    get_contacts_text,
    get_role_intro,
    get_section_text,
)
from texts.messages import ABOUT_TEXT, UNKNOWN_TEXT
from utils.formatters import (
    format_discipline_card,
    format_teacher_card_for_student,
    format_teacher_card_for_teacher,
    format_teacher_short_button_text,
)
from utils.safe_send import safe_message_answer, safe_callback_answer

router = Router(name=__name__)
kb = KnowledgeBase()


@router.message(Command("about"))
@router.message(F.text == "ℹ️ О кафедре")
async def cmd_about(message: Message) -> None:
    await safe_message_answer(
        message,
        ABOUT_TEXT,
        reply_markup=get_main_menu_keyboard(),
    )


@router.message(Command("contacts"))
@router.message(F.text == "📞 Контакты")
async def cmd_contacts(message: Message) -> None:
    await safe_message_answer(
        message,
        get_contacts_text(),
        reply_markup=get_main_menu_keyboard(),
    )


@router.message(F.text == "🎓 Абитуриент")
async def applicant_entry(message: Message) -> None:
    await safe_message_answer(
        message,
        get_role_intro("applicant"),
        reply_markup=get_applicant_menu_inline(),
    )


@router.message(F.text == "📚 Студент")
async def student_entry(message: Message) -> None:
    await safe_message_answer(
        message,
        get_role_intro("student"),
        reply_markup=get_student_menu_inline(),
    )


@router.message(F.text == "👨‍🏫 Преподаватель")
async def teacher_entry(message: Message) -> None:
    await safe_message_answer(
        message,
        get_role_intro("teacher"),
        reply_markup=get_teacher_menu_inline(),
    )


@router.message(F.text == "Общая информация")
@router.message(F.text == "📂 Общая информация")
async def common_entry(message: Message) -> None:
    await safe_message_answer(
        message,
        get_common_menu_text(),
    )


@router.callback_query(F.data == "nav:student:curriculum_subjects")
async def show_courses_for_disciplines(callback: CallbackQuery) -> None:
    courses = kb.get_courses()

    buttons = []
    for course in courses:
        course_number = course.get("course_number")
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{course_number} курс",
                    callback_data=f"disc:course:{course_number}",
                )
            ]
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await safe_callback_answer(
        callback,
        "📚 Выберите курс:",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("disc:course:"))
async def show_semesters_for_course(callback: CallbackQuery) -> None:
    if not callback.data:
        await callback.answer()
        return

    course_number = int(callback.data.split(":")[2])
    semesters = kb.get_semesters_by_course(course_number)

    buttons = []
    for semester in semesters:
        semester_number = semester.get("semester_number")
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{semester_number} семестр",
                    callback_data=f"disc:semester:{course_number}:{semester_number}",
                )
            ]
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await safe_callback_answer(
        callback,
        f"📘 {course_number} курс: выберите семестр",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("disc:semester:"))
async def show_disciplines_for_semester(callback: CallbackQuery) -> None:
    if not callback.data:
        await callback.answer()
        return

    _, _, course_number_str, semester_number_str = callback.data.split(":")
    course_number = int(course_number_str)
    semester_number = int(semester_number_str)

    disciplines = kb.get_disciplines_by_course_and_semester(
        course_number,
        semester_number,
    )

    buttons = []
    for disc in disciplines:
        title = disc.get("name", "")
        hours = disc.get("hours", "")
        button_text = f"{title} ({hours} ч.)"

        if len(button_text) > 64:
            button_text = f"{title[:42]}..."

        buttons.append(
            [
                InlineKeyboardButton(
                    text=button_text,
                    callback_data=f"disc:item:{disc.get('id')}",
                )
            ]
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await safe_callback_answer(
        callback,
        f"📖 {course_number} курс, {semester_number} семестр: выберите дисциплину",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("disc:item:"))
async def show_discipline_card(callback: CallbackQuery) -> None:
    if not callback.data:
        await callback.answer()
        return

    disc_id = callback.data.split(":")[2]
    discipline = kb.get_discipline_by_id(disc_id)

    if not discipline:
        await callback.answer("Дисциплина не найдена")
        return

    teacher = None
    teacher_id = discipline.get("teacher_id")
    if teacher_id:
        teacher = kb.get_teacher_by_id(teacher_id)

    text = format_discipline_card(discipline, teacher)

    await safe_callback_answer(callback, text)
    await callback.answer()


@router.callback_query(F.data == "nav:student:teachers_list")
async def show_teachers_for_students(callback: CallbackQuery) -> None:
    teachers = kb.get_all_teachers()

    buttons = []
    for teacher in teachers:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=format_teacher_short_button_text(teacher),
                    callback_data=f"teachercard:student:{teacher.get('id')}",
                )
            ]
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await safe_callback_answer(
        callback,
        "👨‍🏫 Выберите преподавателя:",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data == "nav:teacher:teachers_staff")
async def show_teachers_for_teachers(callback: CallbackQuery) -> None:
    teachers = kb.get_all_teachers()

    buttons = []
    for teacher in teachers:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=format_teacher_short_button_text(teacher),
                    callback_data=f"teachercard:teacher:{teacher.get('id')}",
                )
            ]
        )

    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await safe_callback_answer(
        callback,
        "👨‍🏫 Выберите преподавателя из состава кафедры:",
        reply_markup=keyboard,
    )
    await callback.answer()


@router.callback_query(F.data.startswith("teachercard:student:"))
async def show_teacher_card_for_student_callback(callback: CallbackQuery) -> None:
    if not callback.data:
        await callback.answer()
        return

    teacher_id = callback.data.split(":")[2]
    teacher = kb.get_teacher_by_id(teacher_id)

    if not teacher:
        await callback.answer("Преподаватель не найден")
        return

    await safe_callback_answer(
        callback,
        format_teacher_card_for_student(teacher),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("teachercard:teacher:"))
async def show_teacher_card_for_teacher_callback(callback: CallbackQuery) -> None:
    if not callback.data:
        await callback.answer()
        return

    teacher_id = callback.data.split(":")[2]
    teacher = kb.get_teacher_by_id(teacher_id)

    if not teacher:
        await callback.answer("Преподаватель не найден")
        return

    await safe_callback_answer(
        callback,
        format_teacher_card_for_teacher(teacher),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("nav:"))
async def process_navigation(callback: CallbackQuery) -> None:
    if not callback.data:
        await callback.answer()
        return

    _, role, section = callback.data.split(":", maxsplit=2)
    text = get_section_text(role=role, section=section)

    if text:
        await safe_callback_answer(callback, text)

    await callback.answer()


@router.message()
async def fallback_message(message: Message) -> None:
    await safe_message_answer(
        message,
        UNKNOWN_TEXT,
        reply_markup=get_main_menu_keyboard(),
    )