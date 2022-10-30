
# General FastAPI Imports
from fastapi import Depends, FastAPI
from fastapi.security.api_key import APIKey
# Enable the live feed 
from multiprocessing import Process, Value
from bussie_backend.data_collection.livestream import enable_live_feed
# Enable the client API

"""
This is the main FastAPI Script

It consists of some imports, then starts the webserver. 
It also starts datacollection and a scheduler which runs specific tasks at a specific interval. 
The combination of these three allows us to run the backend. 
"""

from bussie_backend.client_service import client_api
# Import modules to run on an interval
from apscheduler.schedulers.background import BackgroundScheduler
from utils.recurring_functions.background_tasks import *

#Kickstart a FastAPI process
app = FastAPI()

# This adds all the routes in clients_service to this app.
# This is split up on purpose to keep the app tidy. All routes are in client_service
app.include_router(client_api.router, prefix="/API/V1")

# Enable data collection
# This background task collects all location information and stores in in a database



# Have maintanence scheduled
# We have specific recurring tasks running that keep the application nice and tidy
scheduler = BackgroundScheduler()
scheduler.add_job(Every_minute, 'interval', minutes=1)
scheduler.add_job(Every_fifteen_minutes, 'interval', minutes=15)
scheduler.add_job(Every_hour, 'interval', minutes=60)
scheduler.add_job(Every_day, 'interval', hours=24)


# Enable data collection
# This background task collects all location information and stores in in a database


scheduler.start()
