import os
from pathlib import Path

URL = "https://aeza.net/ru/virtual-servers"
CHECK_INTERVAL = int(os.getenv("AEZA_CHECK_INTERVAL", "300"))
USE_TELEGRAM = os.getenv("AEZA_USE_TELEGRAM", "false").lower() == "true"
TELEGRAM_BOT_TOKEN = os.getenv("AEZA_TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
TELEGRAM_CHAT_ID = os.getenv("AEZA_TELEGRAM_CHAT_ID", "YOUR_CHAT_ID_HERE")
LOG_LEVEL = os.getenv("AEZA_LOG_LEVEL", "INFO")
STATE_FILE = Path(os.getenv("AEZA_STATE_FILE", ".aeza-monitor-state.json"))

LOCATION_NAMES = [
    "Moscow",
    "Frankfurt",
    "Paris",
    "Amsterdam",
    "Charlotte",
    "Vienna",
    "Stockholm",
    "London",
    "Helsinki",
    "Saint-Petersburg",
    "Москва",
    "Франкфурт",
    "Париж",
    "Амстердам",
    "Шарлотт",
    "Вена",
    "Стокгольм",
    "Лондон",
    "Хельсинки",
    "Санкт-Петербург",
]
