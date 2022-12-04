
from fastapi import Depends, Request
from bussie_backend.database import crud, models, schemas
from sqlalchemy.orm import Session
from ..database.database import SessionLocal, engine
from ..calculations.calculate_closest_station import calculate_closest_station
import redis
from redis.commands.json.path import Path
from termcolor import colored
import time


from fastapi import APIRouter
rd = redis.Redis(host='localhost', port=6379, db=0)


router = APIRouter()
models.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/')
async def read_root(request: Request):
    print(colored('request', 'green'), colored('on /', 'white'))

    return {"Hello": "World"}


@router.get('/AWSHealthCheck')
async def healthcechk(request: Request):
    print(colored('Healtcheck', 'green'), colored('By AWS', 'white'))

    return {"Status": "Up And Running"}


# Pass the parameters for this function
# like so: http://127.0.0.1:8000/get_closest_stations/?latitude=20?longitude=20
@router.get('/get_closest_stations/')
async def get_closest_station(latitude: float, longitude: float | None = None):
    print(colored('request', 'green'), colored('on /get_closest_stations', 'white'))
    return calculate_closest_station(latitude, longitude)


@router.post("/add_stops_to_database/", response_model=schemas.Stop)
async def create_stop(stop: schemas.StopCreate,
                  db: Session = Depends(get_db)):
    print(colored('request', 'green'), colored('on /add_stops_to_database', 'white'))

    return crud.create_stop(db=db, stop=stop)


@router.get("/get_vehicles")
@router.get("/vehicles")
# We only calculate the new location every 5 seconds and otherwise return a cached version
# of the list of vehicles we stored.
async def get_vehicle_location():
    if rd.exists('cache_vehiclelist'):
        start_time = time.time()
        print(colored('request', 'green'), colored('on /get_vehicles', 'white'), colored('From Cache', 'blue'),'--', (time.time() - start_time)*1000, 'milliseconds')
        return rd.json().get('cache_vehiclelist')
    else:
        response = {}
        start_time = time.time()
        try:
            for key in rd.keys('*'):
                vehicle = rd.json().get(key.decode('utf-8'))
                response[str(key[2:])] = vehicle
            rd.json().set('cache_vehiclelist', Path.root_path(), response)
            rd.expire('cache_vehiclelist', 5)
            print(colored('request', 'green'), colored('on /get_vehicles', 'white'), colored('recalculated', 'red'),'--', (time.time() - start_time)*1000, 'milliseconds')
            return response
        except Exception as e:
            """pass"""
            print(colored('request', 'green'), colored('on /get_vehicles', 'white'), colored('hit except block', 'red'))
            print(e)
