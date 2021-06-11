from os import stat
from .dataloader import load_dataframe
from datetime import datetime, date, timedelta
import pandas as pd
from sklearn.pipeline import Pipeline

class MlManager():
    def __init__(self, regressor, scaler) -> None:
        self.regressor = regressor
        self.scaler = scaler
    
    @staticmethod
    def get_train_data(uuids):
        # Returns three df, one for each target(e5 e10 diesel)
        train_data = load_dataframe(uuids)
        e5 = train_data[["lat", "lng", "hour", "dom", "month", "year", "dow", "e5"]]
        e10 = train_data[["lat", "lng", "hour", "dom", "month", "year", "dow", "e10"]]
        diesel = train_data[["lat", "lng", "hour", "dom", "month", "year", "dow", "diesel"]]
        e5 = e5[e5.e5 > 0.2]
        e10 = e10[e10.e10 > 0.2]
        diesel = diesel[diesel.diesel > 0.2]
        return e5, e10, diesel
    
    @staticmethod
    def get_prediction_points(prediction_date: date, location):
        dts = [datetime(hour=i, year=prediction_date.year, month=prediction_date.month, day=prediction_date.day) for i in range(24)]
        dps = [{"lat": location[0], "lng": location[1], "hour": dt.hour, "dom": dt.day, "month": dt.month, "year": dt.year, "dow": dt.weekday()} for dt in dts]
        return pd.DataFrame(data=dps)
        # Returns a df with datapoints for all 24 hours in the given date which can be fed into the pipeline for prediction
    
    @staticmethod
    def get_test_point(test_data, hour, location):
        # print(test_data)
        candidates = test_data[test_data.hour == hour]
        mean = candidates["e5"].mean()
        data = candidates.iloc[0]
        return {"lat": location[0], "lng": location[1], "hour": hour, "dom": data["dom"], "month": data["month"], "year": data["year"], "dow": data["dow"], "e5": mean}
    
    @staticmethod
    def get_test_data(uuids, location):
        e5, e10, diesel = MlManager.get_train_data(uuids)
        today = date.today()
        yesterday = today - timedelta(days=1)
        test = e5[(e5.dom==yesterday.day)&(e5.month==yesterday.month)&(e5.year==yesterday.year)]
        train = e5[(e5.dom!=yesterday.day)|(e5.month!=yesterday.month)|(e5.year!=yesterday.year)]
        test_points = []
        for hour in range(24):
            try:
                test_points.append(MlManager.get_test_point(test, hour, location))
            except:
                pass
        return train, pd.DataFrame(data=test_points)
        # Returns a train_data of a specific date for training purposes
    
    def create_pipeline(self):
        pipe = Pipeline([("scaler", self.scaler), ("regressor", self.regressor)])
        return pipe