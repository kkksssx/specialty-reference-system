from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_student_menu_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Учебный план", callback_data="nav:student:curriculum_plan")],
            [InlineKeyboardButton(text="Список дисциплин", callback_data="nav:student:curriculum_subjects")],
            [InlineKeyboardButton(text="Преподаватели", callback_data="nav:student:teachers_list")],
            [InlineKeyboardButton(text="Конференции и наука", callback_data="nav:student:science_events")],
        ]
    )