from flask.views import MethodView
from flask_smorest import Blueprint

from app.schemas.price_schemas import PriceRequestSchema, PriceResponseSchema
from app.services.price_service import PriceService

blp = Blueprint(
    name="prices",
    import_name=__name__,
    url_prefix="/prices",
    description="Routes Coinbase cryptocurrency prices",
)


@blp.route("/")
class PriceRoutes(MethodView):
    @blp.arguments(PriceRequestSchema, location="query")
    @blp.response(200, PriceResponseSchema)
    def get(self, query_params: dict):
        base_currency = query_params.get("base_currency")
        currency = query_params.get("currency")
        date = query_params.get("date")
        return PriceService.get_spot_price(base_currency, currency, date)
