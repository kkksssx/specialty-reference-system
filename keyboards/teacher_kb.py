from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_teacher_menu_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Состав кафедры", callback_data="nav:teacher:teachers_staff")],
            [InlineKeyboardButton(text="Научные проекты", callback_data="nav:teacher:science_projects")],
            [InlineKeyboardButton(text="Учебная нагрузка", callback_data="nav:teacher:curriculum_load")],
            [InlineKeyboardButton(text="О специальности", callback_data="nav:teacher:common_about")],
        ]
    )