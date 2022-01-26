from app.clients.coinbase_client import CoinbaseClient
from app.models.coinbase_pro_report_header import CoinbaseProReportHeader
from app.utils.csv_util import read_csv
from app.utils.list_util import split_in_chunks
from app.utils.time_util import extract_date


class ReportService:
    @staticmethod
    def parse_report(file_bytes: bytes):
        return read_csv(file_bytes)

    @classmethod
    def hydrate_transactions(cls, transactions: list):
        profit = 0
        hydrated_transactions = []
        for transaction in transactions:
            base_currency = transaction.get(CoinbaseProReportHeader.BASE_CURRENCY).lower()
            # Filter out base currency transactions, like USD deposits and fees
            if base_currency != CoinbaseClient.default_currency:
                hydrated_transaction = ReportService.hydrate_transaction(transaction)
                profit += float(hydrated_transaction.get("profit", 0))
                hydrated_transactions.append(hydrated_transaction)
        return hydrated_transactions, profit

    @staticmethod
    def hydrate_transaction(transaction: dict):
        base_currency = transaction.get(CoinbaseProReportHeader.BASE_CURRENCY).lower()
        transaction_type = transaction.get(CoinbaseProReportHeader.TYPE).lower()
        date = extract_date(transaction.get(CoinbaseProReportHeader.DATETIME))
        amount = float(transaction.get(CoinbaseProReportHeader.AMOUNT))
        base_price = float(CoinbaseClient.get_spot_price(base_currency, date=date).get("price"))
        base_value = base_price * amount
        current_price = float(CoinbaseClient.get_spot_price(base_currency).get("price"))
        current_value = current_price * amount
        profit = current_value - base_value
        return {
            "datetime": datetime,
            "type": transaction_type,
            "base_currency": base_currency,
            "currency": CoinbaseClient.default_currency,
            "amount": str(amount),
            "base_value": str(base_value),
            "current_value": str(current_value),
            "profit": str(profit),
        }
