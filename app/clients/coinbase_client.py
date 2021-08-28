import grequests
import requests
from requests import Response
from werkzeug.exceptions import abort


class CoinbaseClient:
    __base_url = "https://api.coinbase.com/v2"
    __prices_base_url = f"{__base_url}/prices"
    default_currency = "usd"

    @classmethod
    def get_spot_price(cls, base_currency: str, currency: str, date: str = None):
        query_params = {"date": date} if date else {}
        response = requests.get(
            f"{cls.__prices_base_url}/{base_currency}-{currency}/spot",
            params=query_params,
        )
        return cls.__extract_price(response)

    @classmethod
    def get_spot_price_async(cls, base_currency: str, currency: str = None, date: str = None):
        currency = currency or cls.default_currency
        query_params = {"date": date} if date else {}
        return grequests.get(
            f"{cls.__prices_base_url}/{base_currency}-{currency}/spot", params=query_params
        )

    @classmethod
    def resolve_spot_price_requests(cls, async_requests: list):
        responses = grequests.map(async_requests)
        return [cls.__extract_price(response) for response in responses]

    @staticmethod
    def __extract_price(response: Response):
        response_dict = response.json()
        if not response.ok:
            abort(response.status_code, response_dict["errors"])
        return {"price": response_dict.get("data").get("amount")}
