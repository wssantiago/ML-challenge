"""Endpoint para cálculo de Performance."""
from utils.reads import read_model, split_df
from fastapi import APIRouter
from sklearn.metrics import f1_score, precision_score, recall_score, mean_squared_error, r2_score
import time
from scipy.stats import pearsonr

# Setting the logger formatting and poiting to correct file.
import logging
logging.basicConfig(filename='../monitoring.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

router = APIRouter(prefix="/performance")


# Calculates the evaluation metric (F1) for the classifier
def get_f1(X_test, y_test, model):
    logging.info("Calculating the F1 score for the requested dataset...")
    try:
        f1 = f1_score(model.predict(X_test), y_test)

        logging.info(
            "Successfully calculated the F1 evaluation metric for the classifier!")
        return {"f1": str(f1)}
    except ValueError as verr:
        logging.error(
            "ValueError exception raised while trying to define F1 score")


# Calculates the satisficing requirements for the classification model
def get_class_satisficing(X_test, y_test, model):
    logging.info("Calculating the satisficing metrics for the classifier on the requested dataset...")
    try:
        start_time = time.time()
        y_pred = model.predict(X_test)
        end_time = time.time()

        precision = precision_score(y_pred, y_test)
        recall = recall_score(y_pred, y_test)
        latency_ms = (end_time - start_time) * 1000

        logging.info(
            "Successfully defined the satisficing metrics!")
        return {"precision": str(precision), "recall": str(recall), "latency_ms": str(latency_ms)}
    except ValueError as verr:
        logging.error(
            "ValueError exception raised while trying to define satisficing metrics")


# Calculates the evaluation metric (RMSE) for the regressor
def get_rmse(X_test, y_test, model):
    logging.info("Calculating the RMSE score for the requested dataset...")
    try:
        rmse = mean_squared_error(y_test, model.predict(X_test), squared=False)

        logging.info(
            "Successfully calculated the RMSE evaluation metric for the regressor!")
        return {"RMSE": str(rmse)}
    except ValueError as verr:
        logging.error(
            "ValueError exception raised while trying to define RMSE score")


# Calculates the satisficing requirements for the regression model
def get_regr_satisficing(X_test, y_test, model):
    logging.info("Calculating the satisficing metrics for the regressor on the requested dataset...")
    try:
        start_time = time.time()
        y_pred = model.predict(X_test)
        end_time = time.time()

        r2 = r2_score(y_test, y_pred)
        corr = pearsonr(y_pred, y_test)
        latency_ms = (end_time - start_time) * 1000

        logging.info(
            "Successfully defined the satisficing metrics!")
        return {"R2": str(r2), "correlation": {"statistic": str(corr.statistic), "p-value": str(corr.pvalue)}, "latency_ms": str(latency_ms)}
    except ValueError as verr:
        logging.error(
            "ValueError exception raised while trying to define satisficing metrics")


# Checks for supported model version and performs
# evaluation and satisficing scores calculation
def calc_performance(model_name: str, json: dict):
    if model_name in ['classifier', 'regressor']:
        model = read_model(model_name)
        X_test, y_test = split_df(json)

        if model_name == 'classifier':
            evaluation_metric = get_f1(X_test, y_test, model)
            satisficing_metrics = get_class_satisficing(X_test, y_test, model)
        else:
            evaluation_metric = get_rmse(X_test, y_test, model)
            satisficing_metrics = get_regr_satisficing(X_test, y_test, model)

        return {'evaluation_metric': evaluation_metric, 'satisficing_metrics': satisficing_metrics}
    return {'evaluation_metric': {}, 'satisficing_metrics': {}}
