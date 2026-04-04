from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from keyboards.main_menu import get_main_menu_keyboard
from keyboards.applicant_kb import get_applicant_menu_inline
from keyboards.student_kb import get_student_menu_inline
from keyboards.teacher_kb import get_teacher_menu_inline
from services.navigation import (
    get_common_menu_text,
    get_contacts_text,
    get_role_intro,
    get_section_text,
)
from texts.messages import ABOUT_TEXT, UNKNOWN_TEXT


router = Router(name=__name__)


@router.message(Command("about"))
@router.message(F.text == "ℹ️ О кафедре")
async def cmd_about(message: Message) -> None:
    await message.answer(ABOUT_TEXT, reply_markup=get_main_menu_keyboard())


@router.message(Command("contacts"))
@router.message(F.text == "📞 Контакты")
async def cmd_contacts(message: Message) -> None:
    await message.answer(get_contacts_text(), reply_markup=get_main_menu_keyboard())


@router.message(F.text == "🎓 Абитуриент")
async def applicant_entry(message: Message) -> None:
    await message.answer(
        get_role_intro("applicant"),
        reply_markup=get_applicant_menu_inline(),
    )


@router.message(F.text == "📚 Студент")
async def student_entry(message: Message) -> None:
    await message.answer(
        get_role_intro("student"),
        reply_markup=get_student_menu_inline(),
    )


@router.message(F.text == "👨‍🏫 Преподаватель")
async def teacher_entry(message: Message) -> None:
    await message.answer(
        get_role_intro("teacher"),
        reply_markup=get_teacher_menu_inline(),
    )


@router.message(F.text == "📂 Общая информация")
async def common_entry(message: Message) -> None:
    await message.answer(get_common_menu_text())


@router.callback_query(F.data.startswith("nav:"))
async def process_navigation(callback: CallbackQuery) -> None:
    if not callback.data:
        await callback.answer()
        return

    _, role, section = callback.data.split(":", maxsplit=2)
    text = get_section_text(role=role, section=section)

    if callback.message:
        await callback.message.answer(text)

    await callback.answer()


@router.message()
async def fallback_message(message: Message) -> None:
    await message.answer(UNKNOWN_TEXT, reply_markup=get_main_menu_keyboard())