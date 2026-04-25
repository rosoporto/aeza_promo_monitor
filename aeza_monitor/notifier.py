import time

import requests

from aeza_monitor.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, USE_TELEGRAM
from aeza_monitor.logging_config import get_logger
from aeza_monitor.models import PromoData

logger = get_logger()


def send_telegram_message(message: str) -> None:
    if not USE_TELEGRAM:
        logger.debug("Telegram notifications are disabled")
        return

    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE" or TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE":
        logger.warning("Telegram is enabled but bot token/chat id are not configured")
        return

    response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        json={"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"},
        timeout=10,
    )
    if response.status_code != 200:
        logger.warning("Telegram API error: %s", response.text)
        return

    logger.info("Telegram notification sent")


def format_console_message(data: PromoData, status: str) -> str:
    if status == "available":
        return (
            f"\n🎉 ТАРИФ PROMO ДОСТУПЕН!\n\n"
            f"📍 Локация: {data.location}\n"
            f"📦 План: {data.plan_code}\n"
            f"💰 Цена: {data.price or 'N/A'}/мес\n\n"
            f"⚙️ Характеристики:\n"
            f"  • CPU: {data.cpu or 'N/A'}\n"
            f"  • RAM: {data.ram or 'N/A'}\n"
            f"  • Disk: {data.disk or 'N/A'}\n"
            f"  • Net: {data.bandwidth or 'N/A'}\n"
            f"  • IPv4: {data.ipv4 or 'N/A'}\n"
            f"  • IPv6: {data.ipv6 or 'N/A'}\n\n"
            f"🔗 Заказать: {data.order_link}\n"
        )

    return (
        f"\n❌ Тариф Promo не найден\n"
        f"⏰ {time.strftime('%H:%M:%S %d.%m.%Y')}\n"
        f"Причина: {data.reason or 'неизвестно'}\n"
    )


def format_telegram_message(data: PromoData, status: str, event: str) -> str:
    if status == "available":
        title = "ТАРИФ PROMO ДОСТУПЕН!"
        if event == "promo_changed":
            title = "PROMO ИЗМЕНИЛСЯ!"

        return (
            f"🎉 <b>{title}</b>\n\n"
            f"📍 <b>Локация:</b> {data.location}\n"
            f"📦 <b>План:</b> {data.plan_code}\n"
            f"💰 <b>Цена:</b> {data.price or 'N/A'}/мес\n\n"
            f"⚙️ <b>Характеристики:</b>\n"
            f"• CPU: {data.cpu or 'N/A'}\n"
            f"• RAM: {data.ram or 'N/A'}\n"
            f"• Disk: {data.disk or 'N/A'}\n"
            f"• Net: {data.bandwidth or 'N/A'}\n"
            f"• IPv4: {data.ipv4 or 'N/A'}\n"
            f"• IPv6: {data.ipv6 or 'N/A'}\n\n"
            f"🔗 <b>Заказать:</b> {data.order_link}"
        )

    return (
        f"❌ <b>Тариф Promo исчез</b>\n\n"
        f"⏰ {time.strftime('%H:%M:%S %d.%m.%Y')}\n"
        f"Причина: {data.reason or 'неизвестно'}"
    )
