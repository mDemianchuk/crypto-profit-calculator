from app.clients.coinbase_client import CoinbaseClient
from app.utils.time_util import get_today


class PriceService:
    default_currency = "usd"

    @classmethod
    def get_spot_price(cls, base_currency: str, currency: str = None, date: str = None):
        currency = currency or cls.default_currency
        spot_price = CoinbaseClient.get_spot_price(base_currency, currency, date)
        spot_price.update(
            {"base_currency": base_currency, "currency": currency, "date": date or get_today()}
        )
        return spot_price
