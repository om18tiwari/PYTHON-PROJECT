from typing import Optional


def validate_symbol(symbol: str) -> str:
    if not symbol or not symbol.isalnum():
        raise ValueError("Symbol must be alphanumeric, for example BTCUSDT.")
    return symbol.upper()


def validate_side(side: str) -> str:
    if not side:
        raise ValueError("Side is required: BUY or SELL.")
    normalized = side.strip().upper()
    if normalized not in {"BUY", "SELL"}:
        raise ValueError("Side must be BUY or SELL.")
    return normalized


def validate_order_type(order_type: str) -> str:
    if not order_type:
        raise ValueError("Order type is required: MARKET or LIMIT.")
    normalized = order_type.strip().upper()
    if normalized not in {"MARKET", "LIMIT"}:
        raise ValueError("Order type must be MARKET or LIMIT.")
    return normalized


def validate_quantity(quantity: str) -> float:
    try:
        qty = float(quantity)
    except (TypeError, ValueError):
        raise ValueError("Quantity must be a number.")
    if qty <= 0:
        raise ValueError("Quantity must be greater than zero.")
    return qty


def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    if order_type == "LIMIT":
        if price is None:
            raise ValueError("Price is required for LIMIT orders.")
        try:
            price_value = float(price)
        except (TypeError, ValueError):
            raise ValueError("Price must be a number for LIMIT orders.")
        if price_value <= 0:
            raise ValueError("Price must be greater than zero.")
        return price_value
    return None
