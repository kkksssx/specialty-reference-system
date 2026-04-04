from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_applicant_menu_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Проходные баллы", callback_data="nav:applicant:admissions_scores")],
            [InlineKeyboardButton(text="Документы и поступление", callback_data="nav:applicant:admissions_rules")],
            [InlineKeyboardButton(text="О специальности", callback_data="nav:applicant:common_about")],
            [InlineKeyboardButton(text="Карьера выпускников", callback_data="nav:applicant:graduates_career")],
        ]
    )