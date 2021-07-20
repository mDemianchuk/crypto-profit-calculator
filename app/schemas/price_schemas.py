from marshmallow import Schema, ValidationError, fields, validates

from app.utils.time_util import validate_date


class PriceRequestSchema(Schema):
    base_currency = fields.Str(required=True)
    currency = fields.Str()
    date = fields.Str()

    @validates("date")
    def validate_date(self, value: str):
        validation_error = validate_date(value)
        if validation_error:
            raise ValidationError(validation_error)


class PriceResponseSchema(Schema):
    base_currency = fields.Str(required=True)
    currency = fields.Str(required=True)
    price = fields.Str(required=True)
    date = fields.Str(required=True)
