from flask import Flask
from flask_smorest import Api
from marshmallow import EXCLUDE
from webargs.flaskparser import FlaskParser
from werkzeug.exceptions import HTTPException, InternalServerError

from config import Env, Config
from routes.price_routes import blp as prices_blp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False
    FlaskParser.DEFAULT_UNKNOWN_BY_LOCATION["json"] = EXCLUDE
    api = Api(app)
    api.register_blueprint(prices_blp, url_prefix=Env.BASE_PATH + prices_blp.url_prefix)

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        error_message = e.description
        if hasattr(e, "data"):
            # Extract error message from flask_smorest.abort
            if "message" in e.data:
                error_message = e.data["message"]
            # Extract schema error message from marshmallow.ValidationError
            elif "messages" in e.data:
                error_message = e.data["messages"]
        response = {"code": e.code, "message": error_message, "status": e.name}
        return response, e.code

    @app.errorhandler(Exception)
    def handle_generic_exception(e: Exception):
        return handle_http_exception(InternalServerError(str(e)))

    return app
