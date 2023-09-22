import requests
from requests import Response
from werkzeug.exceptions import abort


class CoinbaseClient:
    __base_url = "https://api.coinbase.com/v2"
    __prices_base_url = f"{__base_url}/prices"

    @classmethod
    def get_spot_price(cls, base_currency: str, currency: str = "usd", date: str = None):
        query_params = {"date": date} if date else {}
        response = requests.get(
            f"{cls.__prices_base_url}/{base_currency}-{currency}/spot",
            params=query_params,
        )
        return cls.__extract_price(response)

    @staticmethod
    def __extract_price(response: Response):
        response_dict = response.json()
        if not response.ok:
            abort(response.status_code, response_dict["errors"])
        return {"price": response_dict.get("data").get("amount")}
