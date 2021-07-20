import csv
import io

import flask
from flask.views import MethodView
from flask_smorest import Blueprint

from app.schemas.report_schemas import ReportUpload

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
        csv_report = report_upload["csv"]
        file_stream = io.StringIO(csv_report.stream.read().decode("UTF8"))
        transactions = list(csv.DictReader(file_stream))
        return flask.jsonify(transactions)
