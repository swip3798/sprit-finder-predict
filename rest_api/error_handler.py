from . import app
import json
import logging


@app.error(404)
def error404(error):
    logging.warn("HTTP-Error {} occured: {}".format(error.status, error.body))
    return json.dumps({
        "status":"ERR",
        "code": 404,
        "message": error.body
    }, separators=(',', ':'))

@app.error(405)
def error405(error):
    logging.warn("HTTP-Error {} occured: {}".format(error.status, error.body))
    return json.dumps({
        "status":"ERR",
        "code": 405,
        "message": error.body
    }, separators=(',', ':'))

@app.error(403)
def error403(error):
    logging.warn("HTTP-Error {} occured: {}".format(error.status, error.body))
    return json.dumps({
        "status":"ERR",
        "code": 403,
        "message": error.body
    }, separators=(',', ':'))

@app.error(400)
def error400(error):
    logging.warn("HTTP-Error {} occured: {}".format(error.status, error.body))
    return json.dumps({
        "status":"ERR",
        "code": 400,
        "message": error.body
    }, separators=(',', ':'))

@app.error(500)
def error500(error):
    logging.warn("HTTP-Error {} occured: {}".format(error.status, error.body))
    return json.dumps({
        "status":"ERR",
        "code": 500,
        "message": error.body,
    }, separators=(',', ':'))