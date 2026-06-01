import hashlib
import hmac
import time
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests


class BinanceAPIError(Exception):
    pass


class BinanceFuturesClient:
    def __init__(self, api_key: str, api_secret: str, base_url: str = None):
        self.api_key = api_key
        self.api_secret = api_secret.encode("utf-8")
        self.base_url = base_url or "https://testnet.binancefuture.com"

    def _get_timestamp(self) -> int:
        return int(time.time() * 1000)

    def _sign(self, params: Dict[str, Any]) -> str:
        query_string = urlencode(params, doseq=True)
        return hmac.new(self.api_secret, query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    def _request(self, method: str, path: str, params: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        headers = {"X-MBX-APIKEY": self.api_key}
        params["timestamp"] = self._get_timestamp()
        params["recvWindow"] = 5000
        params["signature"] = self._sign(params)

        response = requests.request(method, url, params=params, headers=headers, timeout=15)
        try:
            payload = response.json()
        except ValueError:
            raise BinanceAPIError(f"Invalid JSON response from Binance: {response.text}")

        if not response.ok:
            message = payload.get("msg") or payload
            raise BinanceAPIError(f"Binance API error ({response.status_code}): {message}")

        return payload

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: Optional[float] = None,
    ) -> Dict[str, Any]:
        path = "/fapi/v1/order"
        params: Dict[str, Any] = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "newOrderRespType": "FULL",
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        return self._request("POST", path, params)
