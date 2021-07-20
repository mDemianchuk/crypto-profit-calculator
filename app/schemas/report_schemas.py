from flask_smorest import fields
from marshmallow import Schema


class ReportUpload(Schema):
    csv = fields.Upload(required=True)
