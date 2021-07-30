from app.clients.coinbase_client import CoinbaseClient
from app.models.coinbase_pro_report_header import CoinbaseProReportHeader
from app.utils.csv_util import read_csv
from app.utils.time_util import extract_date


class ReportService:
    @staticmethod
    def parse_report(file_bytes: bytes):
        return read_csv(file_bytes)

    @staticmethod
    def hydrate_transactions(transactions: list):
        hydrated_transactions = []
        for transaction in transactions:
            base_currency = transaction.get(CoinbaseProReportHeader.BASE_CURRENCY).lower()
            # Filter out base currency transactions, like USD deposits and fees
            if base_currency != CoinbaseClient.default_currency:
                hydrated_transactions.append(ReportService.hydrate_transaction(transaction))
        return hydrated_transactions

    @staticmethod
    def hydrate_transaction(transaction: dict):
        base_currency = transaction.get(CoinbaseProReportHeader.BASE_CURRENCY).lower()
        transaction_type = transaction.get(CoinbaseProReportHeader.TYPE).lower()
        datetime = transaction.get(CoinbaseProReportHeader.DATETIME)
        date = extract_date(datetime)
        amount = transaction.get(CoinbaseProReportHeader.AMOUNT)
        base_price = CoinbaseClient.get_spot_price(base_currency, date=date).get("price")
        current_price = CoinbaseClient.get_spot_price(base_currency).get("price")
        return {
            "datetime": datetime,
            "type": transaction_type,
            "base_currency": base_currency,
            "currency": CoinbaseClient.default_currency,
            "amount": amount,
            "base_price": base_price,
            "current_price": current_price,
        }
