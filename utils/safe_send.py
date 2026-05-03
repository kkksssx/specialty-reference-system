import asyncio
from typing import Any

from aiogram.exceptions import TelegramAPIError, TelegramRetryAfter
from aiogram.types import Message, CallbackQuery


async def safe_message_answer(message: Message, text: str, **kwargs: Any):
    try:
        return await message.answer(text, **kwargs)
    except TelegramRetryAfter as e:
        # если Telegram попросил подождать — ждём и пробуем ещё раз
        await asyncio.sleep(e.retry_after)
        try:
            return await message.answer(text, **kwargs)
        except TelegramAPIError:
            return None
    except TelegramAPIError:
        # здесь можно подключить логгер, чтобы не потерять ошибку
        return None


async def safe_callback_answer(
    callback: CallbackQuery,
    text: str,
    **kwargs: Any,
):
    if not callback.message:
        return None

    return await safe_message_answer(callback.message, text, **kwargs)