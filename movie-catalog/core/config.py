from pathlib import Path
import logging

BASE_DIR = Path(__file__).resolve().parent.parent
MOVIES_STORAGE_FILEPATH = BASE_DIR / "movies.json"

LOG_LEVEL = logging.INFO
LOG_FORMAT: str = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)

API_TOKENS: frozenset[str] = frozenset(
    {
        "ZDW8kEJNShdnqLXISR108Q",
        "AXv3FwRku_HH7vYN9PJjEw",
    }
)

USERS_DB: dict[str, str] = {
    "Nikolay": "qwerty",
    "Ivan": "password",
}

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0