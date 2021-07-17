import os
import sys
import logging


class Env:
    try:
        BASE_PATH = os.environ["BASE_PATH"]
    except KeyError as e:
        logging.critical(
            f"Environment variable {e} is not set. Could not start the application."
        )
        sys.exit(-1)


class Config:
    API_TITLE = "Crypto Trade Calculator"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = Env.BASE_PATH
