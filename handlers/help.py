from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from texts.messages import HELP_TEXT
from keyboards.main_menu import get_main_menu_keyboard


router = Router(name=__name__)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    await message.answer(
        HELP_TEXT,
        reply_markup=get_main_menu_keyboard(),
    )