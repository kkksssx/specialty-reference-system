from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_applicant_menu_inline() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Проходные баллы", callback_data="nav:applicant:admissions_scores")],
            [InlineKeyboardButton(text="Вступительные и срок обучения", callback_data="nav:applicant:admissions_exams")],  # НОВОЕ
            [InlineKeyboardButton(text="Документы для поступления", callback_data="nav:applicant:admissions_rules")],
            [InlineKeyboardButton(text="Карьера выпускников", callback_data="nav:applicant:graduates_career")],
            [InlineKeyboardButton(text="О специальности", callback_data="nav:applicant:common_about")],
        ]
    )