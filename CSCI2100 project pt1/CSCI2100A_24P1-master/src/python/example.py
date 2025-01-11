#!/usr/bin/env python
from urllib.request import urlopen

import json
import os

API_KEY = os.environ.get("API_KEY")


def market_cap_api(stocks: list[str]):
    stocks_str = ",".join(stocks)
    url = "https://financialmodelingprep.com/api/v3/market-capitalization/{}?apikey={}".format(
        stocks_str, API_KEY)
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


def historical_market_cap_api(stock: str, _from: str, to: str, limit: int):
    url = "https://financialmodelingprep.com/api/v3/historical-price-full/{}?limit={}&from={}&to={}&apikey={}".format(
        stock, limit, _from, to, API_KEY)
    response = urlopen(url)
    data = response.read().decode("utf-8")
    return json.loads(data)


def main():
    print(market_cap_api(["AAPL", "GOOGL"]))
    print(historical_market_cap_api("AAPL", "2021-01-01", "2021-01-10", 10))


if __name__ == "__main__":
    main()
