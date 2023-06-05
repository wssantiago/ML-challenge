"""Endpoint para cálculo de aderência."""
from utils.reads import read_model, split_df
from fastapi import APIRouter
import sys
from scipy.stats import ks_2samp


# Setting the logger formatting and poiting to correct file.
import logging
logging.basicConfig(filename='../monitoring.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

router = APIRouter(prefix="/aderencia")


# This function reads the model, the requested dataset and performs KS test
# together with the reference dataset.
def calc_adherence(model_name: str, json: dict):
    logging.info(
        "Calculating the adherence over the reference training base and the requested input base...")
    if model_name == 'classifier':
        model = read_model(model_name)

        X_ref, _ = split_df(json['reference'])
        X_req, _ = split_df(json['request'])

        # Defining the score distribution for both datasets
        logging.info(
            "Predicting scores distribution for both reference and input bases...")
        score_ref = model.predict_proba(X_ref)
        score_req = model.predict_proba(X_req)

        # The scores are passed as parameters to this scipy function.
        # It executes the KS test and returns the metrics relative
        # to either being samples from different distributions or
        # from the same one.
        distance = ks_2samp(score_ref[:, 1], score_req[:, 1])
        logging.info(
            "Successfully performed the Kolmogorov-Smirnov test over both score distributions using scipy...")

        return {'KStest-result': {'statistic': distance[0], 'p-value': distance[1]}}
    return {'Model version': 'not supported yet...'}
