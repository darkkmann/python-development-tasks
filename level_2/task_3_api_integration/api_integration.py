"""Fetch and display a cryptocurrency spot price from CoinGecko's public API."""
from __future__ import annotations

import argparse

API_URL = "https://api.coingecko.com/api/v3/simple/price"


def fetch_price(asset: str, currency: str, timeout: float = 15) -> float:
    try:
        import requests
    except ImportError as error:
        raise RuntimeError("Install requirements.txt before using this client.") from error
    try:
        response = requests.get(API_URL, params={"ids": asset, "vs_currencies": currency}, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return float(data[asset][currency])
    except requests.RequestException as error:
        raise RuntimeError(f"API request failed: {error}") from error
    except (KeyError, TypeError, ValueError) as error:
        raise RuntimeError("The API returned an unexpected response; check the asset and currency.") from error


def main() -> int:
    parser = argparse.ArgumentParser(description="Display a crypto spot price.")
    parser.add_argument("asset", nargs="?", default="bitcoin", help="CoinGecko asset id, e.g. bitcoin")
    parser.add_argument("currency", nargs="?", default="usd", help="Currency code, e.g. usd")
    args = parser.parse_args()
    try:
        price = fetch_price(args.asset.lower(), args.currency.lower())
    except RuntimeError as error:
        print(f"Error: {error}")
        return 1
    print(f"1 {args.asset.upper()} = {price:,.2f} {args.currency.upper()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
