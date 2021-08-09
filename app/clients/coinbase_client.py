import grequests
from werkzeug.exceptions import abort


class CoinbaseClient:
    __base_url = "https://api.coinbase.com/v2"
    __prices_base_url = f"{__base_url}/prices"
    default_currency = "usd"

    @classmethod
    def get_spot_price_async(cls, base_currency: str, currency: str = None, date: str = None):
        currency = currency or cls.default_currency
        query_params = {"date": date} if date else {}
        return grequests.get(
            f"{cls.__prices_base_url}/{base_currency}-{currency}/spot", params=query_params
        )

    @classmethod
    def resolve_spot_price_requests(cls, async_requests: tuple):
        spot_prices = []
        responses = grequests.map(async_requests)
        for response in responses:
            response_dict = response.json()
            if not response.ok:
                abort(response.status_code, response_dict["errors"])
            spot_prices.append(
                {
                    "price": response_dict.get("data").get("amount"),
                }
            )
        return spot_prices
