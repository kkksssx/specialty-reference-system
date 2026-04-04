from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_menu_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎓 Абитуриент"), KeyboardButton(text="📚 Студент")],
            [KeyboardButton(text="👨‍🏫 Преподаватель")],
            [KeyboardButton(text="📂 Общая информация")],
            [KeyboardButton(text="ℹ️ О кафедре"), KeyboardButton(text="📞 Контакты")],
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите роль или команду",
    )