import pendulum

DATE_FORMAT = "YYYY-MM-DD"


def extract_date(timestamp: str):
    return pendulum.parse(timestamp).to_date_string()


def validate_date(date_string: str, date_format: str = DATE_FORMAT):
    try:
        pendulum.from_format(date_string, date_format)
    except ValueError as e:
        return str(e)
