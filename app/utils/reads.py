import pickle
import pandas as pd


# Reads the specified model using pickle
def read_model(model_name: str):
    try:
        model_file = open('../models/' + model_name + '.pkl', 'rb')
        model = pickle.load(model_file)

        return model
    except FileNotFoundError as fnf:
        print(fnf)


# Splits the desired dataframe into X and y
def split_df(json: dict):
    test_df = pd.DataFrame(json)
    y_test = test_df.target
    X_test = test_df.drop(columns=['target'])

    return X_test, y_test
