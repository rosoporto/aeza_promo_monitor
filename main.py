import argparse
import asyncio

from aeza_monitor.config import LOG_LEVEL
from aeza_monitor.logging_config import setup_logging
from aeza_monitor.service import check_once, monitor_loop


def parse_args():
    parser = argparse.ArgumentParser(description="Monitor AEZA promo tariff across all locations.")
    parser.add_argument("--once", action="store_true", help="Run a single promo check and exit.")
    return parser.parse_args()


def main():
    setup_logging(LOG_LEVEL)
    args = parse_args()
    if args.once:
        asyncio.run(check_once())
    else:
        asyncio.run(monitor_loop())


if __name__ == "__main__":
    main()
