import json

from aeza_monitor.config import STATE_FILE
from aeza_monitor.logging_config import get_logger
from aeza_monitor.models import NotificationState

logger = get_logger()


def load_state() -> NotificationState:
    if not STATE_FILE.exists():
        logger.info("State file not found, starting with empty notification state")
        return NotificationState()

    try:
        state = NotificationState.from_dict(json.loads(STATE_FILE.read_text(encoding="utf-8")))
        logger.info("Loaded notification state from %s", STATE_FILE)
        return state
    except (OSError, json.JSONDecodeError, TypeError):
        logger.warning("Failed to load state from %s, using empty state", STATE_FILE)
        return NotificationState()


def save_state(state: NotificationState) -> None:
    STATE_FILE.write_text(
        json.dumps(state.to_dict(), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    logger.info("Saved notification state to %s", STATE_FILE)
