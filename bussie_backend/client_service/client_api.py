
from fastapi import Depends, FastAPI, HTTPException, Request
from bussie_backend.database import crud, models, schemas
from sqlalchemy.orm import Session
from ..database.database import SessionLocal, engine
from ..calculations.calculate_closest_station import calculate_closest_station
from ..data_collection.livestream import send_all_location, payload
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import json

from fastapi import APIRouter

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
    print("request on /")
    return {"Hello": "World"}

@router.get('/AWSHealthCheck')
async def read_root(request: Request):
    print("request on /AWSHealthCheck")
    return {"Status": "Up And Running"}

# Pass the parameters for this function
# like so: http://127.0.0.1:8000/get_closest_stations/?latitude=20?longitude=20
@router.get('/get_closest_stations/')
async def get_closest_station(latitude: float, longitude: float | None = None):
    print("request on /get_closest_stations")
    return calculate_closest_station(latitude, longitude)

@router.post("/add_stops_to_database/", response_model=schemas.Stop)
async def create_stop(stop: schemas.StopCreate,
                db: Session = Depends(get_db)):
    print("request on /add_stops_to_database")
    return crud.create_stop(db=db, stop=stop)

@router.get("/get_vehicles")
async def get_vehicle_location():
    print("request on /get_vehicles")
    f = open('vehiclelocations.json')
    data = json.load(f)
    f.close()
    return data
