from app.clients.coinbase_client import CoinbaseClient
from app.models.coinbase_pro_report_header import CoinbaseProReportHeader
from app.utils.csv_util import read_csv
from app.utils.time_util import extract_date


class ReportService:
    __price_cache = {}

    @classmethod
    def __get_currency_pair(cls, base_currency: str, currency: str or None):
        currency = currency or CoinbaseClient.default_currency
        return f"{base_currency}-{currency}"

    @classmethod
    def cache_price(cls, date: str, base_currency: str, price: str, currency: str = None):
        currency_pair = cls.__get_currency_pair(base_currency, currency)
        if currency_pair not in cls.__price_cache:
            cls.__price_cache[currency_pair] = {}
        cls.__price_cache[currency_pair][date] = price

    @classmethod
    def cache_lookup(cls, date: str, base_currency: str, currency: str = None):
        currency_pair = cls.__get_currency_pair(base_currency, currency)
        if currency_pair in cls.__price_cache:
            return cls.__price_cache[currency_pair].get(date)

    @staticmethod
    def parse_report(file_bytes: bytes):
        return read_csv(file_bytes)

    @classmethod
    def hydrate_transactions(cls, transactions: list):
        hydrated_transactions = []
        for transaction in transactions:
            base_currency = transaction.get(CoinbaseProReportHeader.BASE_CURRENCY).lower()
            # Filter out base currency transactions, for example, USD deposits and fees
            if base_currency != CoinbaseClient.default_currency:
                hydrated_transactions.append(cls.hydrate_transaction(transaction))
        return hydrated_transactions

    @classmethod
    def hydrate_transaction(cls, transaction: dict):
        base_currency = transaction.get(CoinbaseProReportHeader.BASE_CURRENCY).lower()
        transaction_type = transaction.get(CoinbaseProReportHeader.TYPE).lower()
        datetime = transaction.get(CoinbaseProReportHeader.DATETIME)
        date = extract_date(datetime)
        amount = transaction.get(CoinbaseProReportHeader.AMOUNT)
        base_price = CoinbaseClient.get_spot_price(base_currency, date=date).get("price")
        current_price = cls.cache_lookup(date, base_currency) or CoinbaseClient.get_spot_price(
            base_currency
        ).get("price")
        cls.cache_price(date, base_currency, current_price)
        return {
            "datetime": datetime,
            "type": transaction_type,
            "base_currency": base_currency,
            "currency": CoinbaseClient.default_currency,
            "amount": amount,
            "base_price": base_price,
            "current_price": current_price,
        }
