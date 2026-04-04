from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from keyboards.student_kb import get_student_menu_inline
from services.navigation import get_role_intro
from services.search import search_for_student
from services.recommendations import get_student_recommendations


router = Router(name=__name__)


@router.message(Command("student"))
async def student_command(message: Message) -> None:
    await message.answer(
        get_role_intro("student"),
        reply_markup=get_student_menu_inline(),
    )


@router.message(Command("recommend"))
async def student_recommend(message: Message) -> None:
    text = get_student_recommendations()
    await message.answer(text)


@router.message(F.text.startswith("студент:"))
@router.message(F.text.startswith("Студент:"))
async def student_search(message: Message) -> None:
    query = message.text.split(":", maxsplit=1)[1].strip()
    result = search_for_student(query)
    await message.answer(result)