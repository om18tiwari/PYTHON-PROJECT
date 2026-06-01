import os

from flask import Flask, flash, render_template, request

from trading_bot.bot.logging_config import setup_logging
from trading_bot.bot.orders import build_order_summary, format_order_response, place_order
from trading_bot.bot.client import BinanceAPIError

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-me")
logger = setup_logging("trading_bot_web.log")


def build_form_values(form):
    return {
        "symbol": form.get("symbol", "BTCUSDT"),
        "side": form.get("side", "BUY"),
        "type": form.get("type", "MARKET"),
        "quantity": form.get("quantity", "0.001"),
        "price": form.get("price", ""),
        "api_key": form.get("api_key", ""),
        "api_secret": form.get("api_secret", ""),
    }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    summary = None
    values = build_form_values(request.form)

    if request.method == "POST":
        symbol = values["symbol"]
        side = values["side"]
        order_type = values["type"]
        quantity = values["quantity"]
        price = values["price"] or None
        api_key = values["api_key"] or os.environ.get("BINANCE_API_KEY")
        api_secret = values["api_secret"] or os.environ.get("BINANCE_API_SECRET")

        try:
            if not api_key or not api_secret:
                raise ValueError(
                    "API credentials are required. Set them in the form or via BINANCE_API_KEY / BINANCE_API_SECRET."
                )

            summary = build_order_summary(symbol, side, order_type, float(quantity), float(price) if price else None)
            logger.info("Web order request: %s", summary.replace("\n", " | "))
            result_data = place_order(
                api_key=api_key,
                api_secret=api_secret,
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
            )
            logger.info("Web order response: %s", result_data)
            result = format_order_response(result_data)
            flash("Order submitted successfully.", "success")
        except (ValueError, BinanceAPIError) as exc:
            logger.error("Web order failed: %s", exc)
            flash(str(exc), "danger")
        except Exception as exc:
            logger.exception("Web order unexpected failure")
            flash(f"Unexpected error: {exc}", "danger")

    return render_template(
        "index.html",
        result=result,
        summary=summary,
        values=values,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
