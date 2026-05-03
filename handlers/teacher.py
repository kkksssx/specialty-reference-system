from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.teacher_kb import get_teacher_menu_inline
from services.navigation import get_role_intro
from services.search import search_teacher

router = Router(name=__name__)


@router.message(Command("teacher"))
async def teacher_command(message: Message) -> None:
    await message.answer(
        get_role_intro("teacher"),
        reply_markup=get_teacher_menu_inline(),
    )


@router.message(F.text.startswith("преподаватель:"))
@router.message(F.text.startswith("Преподаватель:"))
async def teacher_search(message: Message) -> None:
    query = message.text.split(":", maxsplit=1)[1].strip()
    result = search_teacher(query)
    await message.answer(result)