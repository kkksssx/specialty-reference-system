from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.applicant_kb import get_applicant_menu_inline
from services.navigation import get_role_intro
from services.search import search_for_applicant

router = Router(name=__name__)


@router.message(Command("applicant"))
async def applicant_command(message: Message) -> None:
    await message.answer(
        get_role_intro("applicant"),
        reply_markup=get_applicant_menu_inline(),
    )


@router.message(F.text.startswith("абитуриент:"))
@router.message(F.text.startswith("Абитуриент:"))
async def applicant_search(message: Message) -> None:
    query = message.text.split(":", maxsplit=1)[1].strip()
    result = search_for_applicant(query)
    await message.answer(result)