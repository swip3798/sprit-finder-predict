from bottle import Bottle
import os
HTTP_ORIGIN = os.getenv("HTTP_ORIGIN")
MAX_STATIONS = int(os.getenv("MAX_STATIONS", 7))

app = Bottle()

from .predict import predict_model
from .error_handler import error404, error400, error403, error500

