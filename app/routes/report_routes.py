import flask
from flask.views import MethodView
from flask_smorest import Blueprint

from app.schemas.report_schemas import ReportUpload
from app.services.report_service import ReportService

blp = Blueprint(
    name="reports",
    import_name=__name__,
    url_prefix="/reports",
    description="Routes for analyzing transactions reports",
)


@blp.route("/")
class ReportRoutes(MethodView):
    @blp.arguments(ReportUpload, location="files")
    def post(self, report_upload: dict):
        csv_report = report_upload.get("csv")
        transactions = ReportService.parse_report(csv_report.read())
        hydrated_transactions, profit = ReportService.hydrate_transactions(transactions)
        return flask.jsonify({"profit": profit, "transactions": hydrated_transactions})
