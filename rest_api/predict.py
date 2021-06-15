from . import MAX_STATIONS, app, HTTP_ORIGIN
from bottle import request, abort
import time
from machine_learning import MlManager, scaler, perlman, hopper
import utils
from datetime import date
import logging

AVAILABLE_MODELS = {
    "perlman": perlman,
    "hopper": hopper
}

def run_ml_model(model_name, uuids, location):
    starttime = time.time()
    model = AVAILABLE_MODELS[model_name]
    mlm = MlManager(model(), scaler())
    e5, e10, diesel = MlManager.get_train_data(uuids)
    datapulltime = time.time() - starttime
    starttime = time.time()
    train_data = {
        "e5": e5,
        "e10": e10,
        "diesel": diesel
    }
    predictions = {}
    prediction_points = MlManager.get_prediction_points(date.today(), location)
    for gas_type in train_data:
        pipeline = mlm.create_pipeline()
        X, y = utils.get_input_target(train_data[gas_type])
        pipeline.fit(X,y)
        prediction = pipeline.predict(prediction_points)
        prediction = [i[0] for i in prediction]
        predictions[gas_type] = prediction
    predict_time = time.time()-starttime
    runtime = predict_time + datapulltime
    logging.info("Hour prediction called; Model: {}; Running time: {}; Time to predict: {}; Time to pull data: {}; IDs count: {};".format(model_name, runtime, predict_time, datapulltime, len(uuids)))
    return {
        "status": "OK",
        "model_name": model_name,
        "runtime": runtime,
        "time_to_predict": predict_time,
        "time_to_pull_data": datapulltime,
        "hourly_predictions": predictions
    }

@app.route("/predict/<model_name>", method=["POST", "OPTIONS"])
def predict_model(model_name):
    origin = request.headers.get("Origin")
    if request.method != "OPTIONS":
        #if origin != HTTP_ORIGIN and HTTP_ORIGIN != None:
        #    abort(403, "Access denied")
        if model_name not in AVAILABLE_MODELS:
            abort(404, "Model '{}' does not exist".format(model_name))
        if request.json == None:
            abort(400, "Post body must be JSON-encoded")
        location = request.json["location"]
        if type(location) is not list or len(location) != 2:
            abort(400, "Location format wrong")
        station_uuids = request.json["station_uuids"]
        if type(station_uuids) is not list:
            abort(400, "Station UUIDS are not a list")
        if len(station_uuids) == 0:
            abort(400, "Station UUIDS are empty")
        if len(station_uuids) > MAX_STATIONS:
            station_uuids = station_uuids[:MAX_STATIONS]
        if len(station_uuids) == 0:
            abort(400, "Station UUIDS are empty")
        return run_ml_model(model_name, station_uuids, location)
