import argparse
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR.parent) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR.parent))

from trading_bot.bot.logging_config import setup_logging
from trading_bot.bot.orders import build_order_summary, format_order_response, place_order
from trading_bot.bot.client import BinanceAPIError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Place Binance Futures (USDT-M) MARKET or LIMIT orders on the testnet."
    )
    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT"], help="Order type")
    parser.add_argument("--quantity", required=True, help="Order quantity")
    parser.add_argument("--price", help="Price for LIMIT orders")
    parser.add_argument("--api-key", help="Binance API key. If omitted, uses BINANCE_API_KEY env var.")
    parser.add_argument(
        "--api-secret",
        help="Binance API secret. If omitted, uses BINANCE_API_SECRET env var.",
    )
    parser.add_argument(
        "--base-url",
        default="https://testnet.binancefuture.com",
        help="Binance Futures testnet base URL.",
    )
    return parser.parse_args()


def load_credentials(args: argparse.Namespace) -> tuple[str, str]:
    api_key = args.api_key or os.environ.get("BINANCE_API_KEY")
    api_secret = args.api_secret or os.environ.get("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        raise ValueError(
            "API credentials are required. Provide --api-key/--api-secret or set BINANCE_API_KEY and BINANCE_API_SECRET."
        )
    return api_key, api_secret


def main() -> int:
    logger = setup_logging()
    try:
        args = parse_args()
        api_key, api_secret = load_credentials(args)

        logger.info("Placing order: %s %s %s %s %s", args.symbol, args.side, args.type, args.quantity, args.price)
        print(build_order_summary(args.symbol, args.side, args.type, float(args.quantity), float(args.price) if args.price else None))

        response = place_order(
            api_key=api_key,
            api_secret=api_secret,
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price,
            base_url=args.base_url,
        )

        logger.info("Order response: %s", response)
        print(format_order_response(response))
        print("SUCCESS: Order submitted.")
        return 0

    except ValueError as err:
        logger.error("Validation error: %s", err)
        print(f"INPUT ERROR: {err}")
        return 1
    except BinanceAPIError as err:
        logger.error("Binance API error: %s", err)
        print(f"API ERROR: {err}")
        return 2
    except Exception as err:
        logger.exception("Unexpected failure")
        print(f"UNEXPECTED ERROR: {err}")
        return 3


if __name__ == "__main__":
    sys.exit(main())
