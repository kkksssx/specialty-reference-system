import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    bot_token: str
    bot_name: str = "Интеллектуальная справочная система"
    parse_mode: str = "HTML"


def load_config() -> Settings:
    bot_token = os.getenv("BOT_TOKEN", "").strip()
    bot_name = os.getenv("BOT_NAME", "Интеллектуальная справочная система").strip()

    if not bot_token:
        raise ValueError("Не найден BOT_TOKEN в .env")

    return Settings(
        bot_token=bot_token,
        bot_name=bot_name,
    )


settings = load_config()