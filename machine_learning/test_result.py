from sklearn.metrics import explained_variance_score, median_absolute_error, mean_absolute_error, mean_squared_error, mean_squared_log_error, r2_score
import pandas as pd

class TestResult():

    def __init__(self, targets, predictions, model = None):
        self.targets = targets.iloc[:,0]
        self.predictions = [i[0] for i in predictions]
        self.model = model
        self.median_absolute_error = median_absolute_error(targets, predictions)
        self.mean_absolute_error = mean_absolute_error(targets, predictions)
        self.mean_squared_error = mean_squared_error(targets, predictions)
        self.mean_squared_log_error = mean_squared_log_error(targets, predictions)
        self.explained_variance_score = explained_variance_score(targets, predictions)
        self.r2_score = r2_score(targets, predictions)

    def get_sns_data(self):
        targetdf = pd.concat([pd.Series(self.targets.tolist(), name="Value"), pd.Series(["Actual" for i in range(len(self.targets))], name="Type")], axis=1)
        predicdf = pd.concat([pd.Series(self.predictions, name="Value"), pd.Series(["Predictions" for i in range(len(self.predictions))], name="Type")], axis=1)
        return pd.concat([targetdf, predicdf])
    
    def print_report(self):
        print("####################################################")
        print("Evaluation report of model:", self.model.__class__.__name__)
        print("----------------------------------------------------")
        print("Total number of test samples:", len(self.targets))
        print("")
        print("Explained variance score:", self.explained_variance_score)
        print("Mean absolute error:", self.mean_absolute_error)
        print("Mean squared error:", self.mean_squared_error)
        print("Mean squared logarithmic error:", self.mean_squared_log_error)
        print("Median absolute error:", self.median_absolute_error)
        print("R2 score:", self.r2_score)
        print("####################################################")
        print("")
    
    def get_dict_report(self):
        return {
            "median_absolute_error": self.median_absolute_error,
            "explained_variance_score": self.explained_variance_score,
            "mean_absolute_error": self.mean_absolute_error,
            "mean_squared_error": self.mean_squared_error,
            "mean_squared_log_error": self.mean_squared_log_error,
            "r2_score": self.r2_score,
        }