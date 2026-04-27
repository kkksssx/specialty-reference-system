import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv

from handlers import register_all_routers


async def main() -> None:
    load_dotenv()
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise ValueError("Не найден BOT_TOKEN в .env")

    bot = Bot(
        token=token,
        default=DefaultBotProperties(parse_mode="HTML"),
    )
    dp = Dispatcher()

    register_all_routers(dp)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())