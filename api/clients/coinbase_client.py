import requests
from werkzeug.exceptions import abort

from utils.date_util import get_today


class CoinbaseClient:
    __base_url = "https://api.coinbase.com/v2"
    __prices_base_url = f"{__base_url}/prices"
    __default_currency = "usd"

    @classmethod
    def get_spot_price(cls, base_currency: str, currency: str = None, date: str = None):
        currency = currency or cls.__default_currency
        date = date or get_today()
        response = requests.get(
            f"{cls.__prices_base_url}/{base_currency}-{currency}/spot",
            params={"date": date},
        )
        response_dict = response.json()
        if response.ok:
            return {
                "base_currency": base_currency,
                "currency": currency,
                "price": response_dict.get("data").get("amount"),
                "date": date,
            }
        else:
            abort(response.status_code, response_dict["errors"])
