import requests
from werkzeug.exceptions import abort

from app.utils.time_util import get_today


class CoinbaseClient:
    __base_url = "https://api.coinbase.com/v2"
    __prices_base_url = f"{__base_url}/prices"
    default_currency = "usd"

    @classmethod
    def get_spot_price(cls, base_currency: str, currency: str = None, date: str = None):
        currency = currency or cls.default_currency
        query_params = {"date": date} if date else {}
        response = requests.get(
            f"{cls.__prices_base_url}/{base_currency}-{currency}/spot",
            params=query_params,
        )
        response_dict = response.json()
        if not response.ok:
            abort(response.status_code, response_dict["errors"])
        return {
            "base_currency": base_currency,
            "currency": currency,
            "price": response_dict.get("data").get("amount"),
            "date": date or get_today(),
        }
