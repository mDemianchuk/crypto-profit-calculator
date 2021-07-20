from app.clients.coinbase_client import CoinbaseClient
from app.models.coinbase_pro_report_header import CoinbaseProReportHeader
from app.utils.time_util import extract_date


class ReportService:
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
        amount = float(transaction.get(CoinbaseProReportHeader.AMOUNT))
        base_price = float(CoinbaseClient.get_spot_price(base_currency, date=date).get("price"))
        base_value = base_price * amount
        current_price = float(CoinbaseClient.get_spot_price(base_currency).get("price"))
        current_value = current_price * amount
        value_difference = current_value - base_value
        return {
            "datetime": datetime,
            "type": transaction_type,
            "base_currency": base_currency,
            "currency": CoinbaseClient.default_currency,
            "amount": str(amount),
            "base_value": str(base_value),
            "current_value": str(current_value),
            "value_difference": str(value_difference),
        }
