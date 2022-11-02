
from fastapi import FastAPI, Request
from bussie_backend.data_collection.livestream import worker
from bussie_backend.client_service import client_api
from apscheduler.schedulers.background import BackgroundScheduler
#from utils.recurring_functions.background_tasks import Every_minute, Every_fifteen_minutes, Every_hour, Every_day
import uvicorn
import multiprocessing
import time
from bussie_backend.calculations.Rijksdriekhoek_To_LatLon import convert


# Defining the fastapi object
app = FastAPI()

# This adds all the routes in clients_service to this app.
# This is split up on purpose to keep the app tidy. All routes are in client_service
app.include_router(client_api.router, prefix="/API/V1")

# Simple test route used to see if we're running 
# TO DO: replace with real homepage
@app.get("/")
async def root():
    print("request on /")
    return {"message": "Hello World"}

#Define server function
def server():
    uvicorn.run(app, host="0.0.0.0", port=80)

# starting all processes here
if __name__ == '__main__':
    # Runs api server and datastream worker in separate processes
    print("Starting the Webserver")
    webserver = multiprocessing.Process(target=server)
    webserver.start()
    print("Starting the Datastream")
    time.sleep(1)  # Wait for server to start
    datastream = multiprocessing.Process(target=worker)
    datastream.start()
    webserver.join()
    datastream.join()