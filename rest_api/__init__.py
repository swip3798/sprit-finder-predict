from bottle import Bottle, response
import os
HTTP_ORIGIN = os.getenv("HTTP_ORIGIN")
MAX_STATIONS = int(os.getenv("MAX_STATIONS", 7))

app = Bottle()

from .predict import predict_model
from .error_handler import error404, error400, error403, error500

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@app.route("/status")
def status():
    return {
        "status": "OK"
    }