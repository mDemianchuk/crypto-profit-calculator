from app.clients.coinbase_client import CoinbaseClient
from app.models.coinbase_pro_report_header import CoinbaseProReportHeader
from app.utils.csv_util import read_csv
from app.utils.list_util import split_in_chunks
from app.utils.time_util import extract_date, get_today


class ReportService:
    @staticmethod
    def parse_report(file_bytes: bytes):
        return read_csv(file_bytes)

    @classmethod
    def hydrate_transactions(cls, transactions: list):
        hydrated_transactions = cls.map_transactions(transactions)
        current_price_requests = []
        current_prices = []
        base_price_requests = []
        base_prices = []

        for transaction in hydrated_transactions:
            base_currency = transaction.get("base_currency")
            datetime = transaction.get("datetime")
            date = extract_date(datetime)
            base_price_requests.append(
                CoinbaseClient.get_spot_price_async(base_currency, date=date)
            )
            current_price_requests.append((CoinbaseClient.get_spot_price_async(base_currency)))

        for async_requests in split_in_chunks(current_price_requests):
            current_prices += CoinbaseClient.resolve_spot_price_requests(async_requests)

        for async_requests in split_in_chunks(base_price_requests):
            base_prices += CoinbaseClient.resolve_spot_price_requests(async_requests)

        for (
            transaction,
            current_price,
            base_price,
        ) in zip(hydrated_transactions, current_prices, base_prices):
            transaction["current_price"] = current_price["price"]
            transaction["base_price"] = base_price["price"]

        return hydrated_transactions

    @classmethod
    def map_transactions(cls, transactions: list):
        mapped_transactions = []
        for transaction in transactions:
            base_currency = transaction.get(CoinbaseProReportHeader.BASE_CURRENCY).lower()
            # Filter out base currency transactions, for example, USD deposits and fees
            if base_currency != CoinbaseClient.default_currency:
                mapped_transactions.append(cls.map_transaction(transaction))
        return mapped_transactions

    @classmethod
    def map_transaction(cls, transaction: dict):
        base_currency = transaction.get(CoinbaseProReportHeader.BASE_CURRENCY).lower()
        transaction_type = transaction.get(CoinbaseProReportHeader.TYPE).lower()
        datetime = transaction.get(CoinbaseProReportHeader.DATETIME)
        amount = transaction.get(CoinbaseProReportHeader.AMOUNT)
        return {
            "datetime": datetime,
            "type": transaction_type,
            "base_currency": base_currency,
            "currency": CoinbaseClient.default_currency,
            "amount": amount,
        }
