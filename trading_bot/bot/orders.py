from typing import Any, Dict, Optional

from trading_bot.bot.client import BinanceFuturesClient
from trading_bot.bot.validators import (
    validate_order_type,
    validate_price,
    validate_quantity,
    validate_side,
    validate_symbol,
)


def build_order_summary(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float],
) -> str:
    lines = [
        "Order Request Summary:",
        f"  Symbol: {symbol}",
        f"  Side: {side}",
        f"  Type: {order_type}",
        f"  Quantity: {quantity}",
    ]
    if price is not None:
        lines.append(f"  Price: {price}")
    return "\n".join(lines)


def format_order_response(response: Dict[str, Any]) -> str:
    executed_qty = response.get("executedQty", "N/A")
    avg_price = response.get("avgPrice", "N/A")
    status = response.get("status", "N/A")
    order_id = response.get("orderId", "N/A")
    return (
        "Order Response Details:\n"
        f"  orderId: {order_id}\n"
        f"  status: {status}\n"
        f"  executedQty: {executed_qty}\n"
        f"  avgPrice: {avg_price}"
    )


def place_order(
    api_key: str,
    api_secret: str,
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None,
    base_url: str = None,
) -> Dict[str, Any]:
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    quantity_value = validate_quantity(quantity)
    price_value = validate_price(price, order_type)

    client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret, base_url=base_url or None)
    return client.place_order(symbol=symbol, side=side, order_type=order_type, quantity=quantity_value, price=price_value)
