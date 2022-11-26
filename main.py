
from fastapi import FastAPI, Request
from bussie_backend.data_collection.livestream import worker
from bussie_backend.client_service import client_api
from apscheduler.schedulers.background import BackgroundScheduler
#from utils.recurring_functions.background_tasks import Every_minute, Every_fifteen_minutes, Every_hour, Every_day
import uvicorn
import multiprocessing
import time
from termcolor import colored
import redis

rd = redis.Redis(host='localhost', port=6379, db=0)



# Defining the fastapi object
app = FastAPI()

# This adds all the routes in clients_service to this app.
# This is split up on purpose to keep the app tidy. All routes are in client_service
app.include_router(client_api.router, prefix="/API/V1")

# Simple test route used to see if we're running 
# TO DO: replace with real homepage
@app.get("/")
async def root():
    print(colored('request', 'green'), colored('on /', 'white'))
    return {"message": "Hello World"}

#Define server function
def server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# starting all processes here
if __name__ == '__main__':
    # Runs api server and datastream worker in separate processes
    print(colored('🌍 Started the Webserver', 'green'), colored('-- Listening for requests', 'white'))
    print(colored('👻 Tip', 'yellow'), colored('-- If you are running locally start a redis container using this command:', 'white'))

    print(colored('          docker run -d --name redis-stack -p 6379:6379 -p 8001:8001 redis/redis-stack:latest', 'blue'))
    webserver = multiprocessing.Process(target=server)
    webserver.start()
    print(colored('📥 Started the datastream', 'green'), colored('-- Listening for Vehicle position data', 'white'))
    time.sleep(1)  # Wait for server to start
    datastream = multiprocessing.Process(target=worker)
    datastream.start()
    webserver.join()
    datastream.join()