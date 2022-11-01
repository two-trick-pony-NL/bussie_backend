
# General FastAPI Imports
from fastapi import Depends, FastAPI, Request
from fastapi.security.api_key import APIKey
# Enable the live feed 
from multiprocessing import Process, pool
from bussie_backend.data_collection.livestream import enable_data_stream
# Enable the client API
from bussie_backend.client_service import client_api
# Import modules to run on an interval
from apscheduler.schedulers.background import BackgroundScheduler
#from utils.recurring_functions.background_tasks import Every_minute, Every_fifteen_minutes, Every_hour, Every_day

"""
This is the main FastAPI Script

It consists of some imports, then starts the webserver. 
It also starts datacollection and a scheduler which runs specific tasks at a specific interval. 
The combination of these three allows us to run the backend. 
"""


def func2():
    #Kickstart a FastAPI process
    app = FastAPI()

    # This adds all the routes in clients_service to this app.
    # This is split up on purpose to keep the app tidy. All routes are in client_service
    app.include_router(client_api.router, prefix="/API/V1")

    @app.get('/')
    def read_root(request: Request):
        return {"Hello": "World"}

# Enable data collection
# This background task collects all location information and stores in in a database
pool = Pool()

p1 = Process(target=enable_data_stream)




# Have maintanence scheduled
# We have specific recurring tasks running that keep the application nice and tidy
"""
scheduler = BackgroundScheduler()
scheduler.add_job(Every_minute, 'interval', minutes=1)
scheduler.add_job(Every_fifteen_minutes, 'interval', minutes=15)
scheduler.add_job(Every_hour, 'interval', minutes=60)
scheduler.add_job(Every_day, 'interval', hours=24)


# Enable data collection
# This background task collects all location information and stores in in a database
scheduler.start()
"""