import os
import requests

BASE_URL = "https://www.alphavantage.co/query"


class PriceLookupError(Exception):
    """Custom exception for price lookup failures."""
    pass


def get_latest_price(ticker: str) -> float:
    # 🔽 Read the key at call time, not import time
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY", "").strip()

    if not api_key:
        raise PriceLookupError("ALPHA_VANTAGE_API_KEY is not set inside the container.")

    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": ticker,
        "apikey": api_key,
    }

    try:
        resp = requests.get(BASE_URL, params=params, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as e:
        raise PriceLookupError(f"Network/API error: {e}") from e

    data = resp.json() or {}
    quote = data.get("Global Quote") or data.get("Global_Quote")

    if not quote:
        raise PriceLookupError("No quote data returned for that ticker.")

    price_str = quote.get("05. price") or quote.get("05. Price")
    if not price_str:
        raise PriceLookupError("Price field missing in API response.")

    try:
        return float(price_str)
    except ValueError as e:
        raise PriceLookupError(f"Invalid price value: {price_str}") from e
