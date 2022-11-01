from multiprocessing.resource_sharer import stop
from sqlalchemy.orm import Session

from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_stop(db: Session, stop: schemas.StopCreate):
    db_stop = models.Stop(TimingPointName=stop.TimingPointName, latitude=stop.latitude, longitude=stop.longitude, StopAreaCode=stop.StopAreaCode, TimingPointTown=stop.TimingPointTown)
    db.add(db_stop)
    db.commit()
    db.refresh(db_stop)
    return db_stop

def create_vehicle(db: Session, timestamp,  operator, linenumber, x_coordinate,  y_coordinate):
    db_vehicle = models.Vehicles(TimeStamp=timestamp, latitude=x_coordinate, longitude=y_coordinate, Operator=operator, LineNumber=linenumber)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

def get_stops(db: Session, skip: int = 0, limit: int = 100000):
    return db.query(models.Stop).offset(skip).limit(limit).all()