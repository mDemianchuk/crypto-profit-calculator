from flask.views import MethodView
from flask_smorest import Blueprint

from clients.coinbase_client import CoinbaseClient
from schemas.price_schemas import PriceRequestSchema, PriceResponseSchema

blp = Blueprint(
    name="prices",
    import_name=__name__,
    url_prefix="/prices",
    description="Routes Coinbase cryptocurrency prices",
)


@blp.route("/")
class PriceRequest(MethodView):
    @blp.arguments(PriceRequestSchema, location="query")
    @blp.response(200, PriceResponseSchema)
    def get(self, query_params: dict):
        base_currency = query_params.get("base_currency")
        currency = query_params.get("currency")
        date = query_params.get("date")
        return CoinbaseClient.get_spot_price(base_currency, currency, date)
