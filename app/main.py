"""Main module."""
import uvicorn
from typing import List
from fastapi import FastAPI, status
from api.routers import router
from api.endpoints.performance import calc_performance
from api.endpoints.aderencia import calc_adherence

# Setting the logger formatting and poiting to correct file.
import logging
logging.basicConfig(filename='./monitoring.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')

app = FastAPI(title='Model monitoring', version="1.0.0")


@app.get("/")
async def read_root():
    """Hello World message."""
    return {"Hello World": "from FastAPI"}


@app.get("/performance/{model}/", status_code=status.HTTP_200_OK)
async def read_performance(model: str):
    return {"Hello World": "from /performance/" + model + "/ endpoint"}


# The POST request calls calc_performance for determining the metrics.
# The request body is defined as a dictionary (JSON representing the CSV data)
# and the response model is a dictionary with both evaluation and satisficing metrics.
@app.post("/performance/{model}/", response_model=dict, status_code=status.HTTP_201_CREATED)
async def write_performance(model: str, json: dict):
    
    logging.info("Starting API post request to /performance/" + model + ".")
    performance = calc_performance(model, json)
    logging.info("Finished POST, performance metrics successfully calculated!")

    return performance


@app.get("/adherence/{model}", status_code=status.HTTP_200_OK)
async def read_adherence(model: str):
    return {"Hello World": "from /adherence/" + model + "/ endpoint"}


# The POST request calls calc_aderencia for determining the metrics.
# The request body is defined as a dictionary, as well as the response model.
# The request one is a dictionary with reference and requested data.
# The response one has keys containing the KS test returned metrics.
@app.post("/adherence/{model}", response_model=dict, status_code=status.HTTP_201_CREATED)
async def write_adherence(model: str, json: dict):

    logging.info("Starting API post request to /adherence/" + model + ".")
    adherence = calc_adherence(model, json)
    logging.info("Finished POST, KStest metrics successfully calculated!")

    return adherence


app.include_router(router, prefix="/v1")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
