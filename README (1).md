# Binance Futures Testnet Trading Bot

Simple Python project for Binance Futures USDT-M testnet orders.

This project can:

- place MARKET and LIMIT orders
- handle BUY and SELL
- run from CLI
- run from browser UI
- validate inputs and log requests

## What you need

- Python 3.9+
- `requests`
- `Flask`

## Setup

1. Go to project folder.
2. Create and activate virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install requirements:

```powershell
pip install -r requirements.txt
```

4. Get Binance Futures Testnet API keys from https://testnet.binancefuture.com.
5. Set env vars or use the form/CLI options:

```powershell
$env:BINANCE_API_KEY = "your_testnet_api_key"
$env:BINANCE_API_SECRET = "your_testnet_api_secret"
```

## Run CLI

From repository root:

```powershell
python trading_bot\cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

Limit order example:

```powershell
python trading_bot\cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 65000
```

Inline credentials:

```powershell
python trading_bot\cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --api-key YOUR_KEY --api-secret YOUR_SECRET
```

## Run browser UI

Start UI:

```powershell
python -m trading_bot.web
```

Open browser:

```text
http://127.0.0.1:5000
```

## What you get

- Order summary
- Response details
- Success or failure message
- Logs in `logs/trading_bot.log`

## Notes

- The project defaults to Binance Futures testnet URL.
- LIMIT orders require `--price` or browser price field.
- Samples are in `samples/market-order.log` and `samples/limit-order.log`.
