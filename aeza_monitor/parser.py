import re

from playwright.async_api import TimeoutError as PlaywrightTimeoutError
from playwright.async_api import async_playwright

from aeza_monitor.config import LOCATION_NAMES, URL
from aeza_monitor.logging_config import get_logger
from aeza_monitor.models import PromoData

logger = get_logger()

PROMO_PATTERN = re.compile(
    r"((?:Promo|Промо).*?(?:[A-Z]{3,}-PROMO).*?(?:month|месяц)\s+\d+(?:[.,]\d+)?\s+€)",
    re.IGNORECASE | re.DOTALL,
)


class AezaPromoParser:
    async def fetch_promo(self) -> PromoData:
        logger.info("Starting promo scan across %s locations", len(LOCATION_NAMES))
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                await page.goto(URL, wait_until="domcontentloaded", timeout=60000)
                await page.wait_for_timeout(3000)

                for location_name in LOCATION_NAMES:
                    button = page.get_by_role("button", name=location_name)
                    if not await button.count():
                        logger.debug("Location button not found: %s", location_name)
                        continue

                    logger.debug("Checking location: %s", location_name)
                    await button.first.click()
                    await page.wait_for_timeout(2500)

                    text = await page.locator("body").inner_text()
                    promo_match = PROMO_PATTERN.search(text)
                    if not promo_match:
                        continue

                    promo_block = promo_match.group(1)
                    if "sold out" in promo_block.lower() or "unavailable" in promo_block.lower():
                        logger.info("Promo block found but unavailable in %s", location_name)
                        continue

                    logger.info("Promo found in location: %s", location_name)
                    return self.parse_promo_block(location_name, promo_block)

                logger.info("Promo not found in any location")
                return PromoData(found=False, reason="Promo tariff not found in any location")
            except PlaywrightTimeoutError as exc:
                logger.warning("Timeout while loading page: %s", exc)
                return PromoData(found=False, reason=f"Timeout while loading page: {exc}")
            except Exception as exc:
                logger.exception("Unexpected parser error")
                return PromoData(found=False, reason=str(exc))
            finally:
                await browser.close()

    def parse_promo_block(self, location_name: str, promo_block: str) -> PromoData:
        cpu_match = re.search(r"(\d+)\s*core", promo_block, re.IGNORECASE)
        ram_match = re.search(r"(\d+(?:\.\d+)?)\s*GB\s*RAM", promo_block, re.IGNORECASE)
        disk_match = re.search(r"(\d+(?:\.\d+)?)\s*GB\s*NVME", promo_block, re.IGNORECASE)
        bandwidth_match = re.search(r"(\d+(?:\.\d+)?)\s*(Mbit|Gbit)/s", promo_block, re.IGNORECASE)
        price_match = re.search(r"(?:month|месяц)\s+(\d+(?:[.,]\d+)?)\s+€", promo_block, re.IGNORECASE)
        plan_match = re.search(r"([A-Z]{3,}-PROMO)", promo_block)
        ipv6_match = re.search(r"(/\d+\s*IPv6(?:\s*(?:subnet|подсеть))?)", promo_block, re.IGNORECASE)

        return PromoData(
            found=True,
            location=location_name,
            name="Promo",
            plan_code=plan_match.group(1) if plan_match else "PROMO",
            price=f"{price_match.group(1)} €" if price_match else None,
            cpu=f"{cpu_match.group(1)} core" if cpu_match else None,
            ram=f"{ram_match.group(1)} GB RAM" if ram_match else None,
            disk=f"{disk_match.group(1)} GB NVME" if disk_match else None,
            bandwidth=(
                f"{bandwidth_match.group(1)} {bandwidth_match.group(2).title()}/s"
                if bandwidth_match
                else None
            ),
            ipv4="1 адрес IPv4" if "IPv4" in promo_block else None,
            ipv6=ipv6_match.group(1) if ipv6_match else None,
            order_link=URL,
        )
