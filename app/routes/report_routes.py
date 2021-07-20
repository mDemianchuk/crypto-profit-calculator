import csv

import flask
from flask.views import MethodView
from flask_smorest import Blueprint

from app.schemas.report_schemas import ReportUpload
from app.services.report_service import ReportService
from app.utils.file_util import to_file_stream

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
        file_stream = to_file_stream(csv_report.read())
        transactions = list(csv.DictReader(file_stream))
        hydrated_transactions = ReportService.hydrate_transactions(transactions)
        return flask.jsonify(hydrated_transactions)
