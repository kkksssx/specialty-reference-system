from aiogram import F, Router
from aiogram.types import Message

from services.search import search_discipline

router = Router(name=__name__)


@router.message(F.text.startswith("дисциплина:"))
@router.message(F.text.startswith("Дисциплина:"))
async def discipline_search(message: Message) -> None:
    query = message.text.split(":", maxsplit=1)[1].strip()
    result = search_discipline(query)
    await message.answer(result)