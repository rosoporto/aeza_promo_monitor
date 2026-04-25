import asyncio

from aeza_monitor.config import CHECK_INTERVAL, URL, USE_TELEGRAM
from aeza_monitor.logging_config import get_logger
from aeza_monitor.models import NotificationState, PromoData
from aeza_monitor.notifier import (
    format_console_message,
    format_telegram_message,
    send_telegram_message,
)
from aeza_monitor.parser import AezaPromoParser
from aeza_monitor.state import load_state, save_state

logger = get_logger()


def detect_event(current: PromoData, last_notified: PromoData | None) -> str:
    if current.found:
        if last_notified is None or not last_notified.found:
            return "promo_found"
        if current.signature() != last_notified.signature():
            return "promo_changed"
        return "no_change"

    if last_notified is not None and last_notified.found:
        return "promo_lost"
    return "no_change"


async def check_once() -> None:
    parser = AezaPromoParser()
    data = await parser.fetch_promo()
    status = "available" if data.found else "unavailable"
    logger.info(format_console_message(data, status))


async def monitor_loop() -> None:
    parser = AezaPromoParser()
    state = load_state()

    logger.info("=" * 60)
    logger.info("МОНИТОРИНГ ТАРИФА AEZA PROMO")
    logger.info("URL: %s", URL)
    logger.info("Интервал проверки: %s сек", CHECK_INTERVAL)
    logger.info("Telegram: %s", "ВКЛЮЧЕН" if USE_TELEGRAM else "ВЫКЛЮЧЕН")
    logger.info("=" * 60)

    while True:
        logger.info("Starting scheduled promo check")
        current = await parser.fetch_promo()
        event = detect_event(current, state.last_notified)
        logger.info("Detected monitor event: %s", event)

        if current.found:
            if event in {"promo_found", "promo_changed"}:
                logger.info(format_console_message(current, "available"))
                send_telegram_message(format_telegram_message(current, "available", event))
                state.last_notified = current
                save_state(state)
            else:
                logger.info(
                    "Promo unchanged (%s, %s)",
                    current.location,
                    current.price or "N/A",
                )
        else:
            if event == "promo_lost":
                logger.info(format_console_message(current, "unavailable"))
                send_telegram_message(format_telegram_message(current, "unavailable", event))
                state.last_notified = current
                save_state(state)
            else:
                logger.info("Promo not found")

        await asyncio.sleep(CHECK_INTERVAL)
