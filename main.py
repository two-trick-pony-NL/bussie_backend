
from fastapi import Depends, FastAPI, Request
from fastapi.security.api_key import APIKey
# Enable the live feed 
from multiprocessing import Process
from bussie_backend.data_collection.livestream import worker
# Enable the client API
from bussie_backend.client_service import client_api
# Import modules to run on an interval
from apscheduler.schedulers.background import BackgroundScheduler
#from utils.recurring_functions.background_tasks import Every_minute, Every_fifteen_minutes, Every_hour, Every_day

import uvicorn
import multiprocessing
import time
import zmq
import xml.etree.ElementTree as ET
from gzip import GzipFile
from io import BytesIO
from fastapi import FastAPI

app = FastAPI()
#Kickstart a FastAPI process

# This adds all the routes in clients_service to this app.
# This is split up on purpose to keep the app tidy. All routes are in client_service
app.include_router(client_api.router, prefix="/API/V1")
@app.get('/')
def read_root(request: Request):
    return {"Hello": "World"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


def server():
    uvicorn.run(app, host="0.0.0.0", port=80)

# Start the server here
if __name__ == '__main__':
    print("Starting the server")
    # Runs api server and datastream worker in separate processes
    webserver = multiprocessing.Process(target=server)
    webserver.start()
    print("Starting the Datastream")
    time.sleep(1)  # Wait for server to start
    datastream = multiprocessing.Process(target=worker)
    datastream.start()
    webserver.join()
    datastream.join()