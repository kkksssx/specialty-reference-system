from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import get_main_menu_keyboard
from texts.welcome import get_welcome_text


router = Router(name=__name__)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(
        get_welcome_text(message.from_user.first_name if message.from_user else None),
        reply_markup=get_main_menu_keyboard(),
    )