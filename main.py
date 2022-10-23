from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security.api_key import APIKey
from sqlalchemy.orm import Session
from bussie_backend.database import crud, models, schemas
from bussie_backend.database.database import SessionLocal, engine
from bussie_backend.calculations.calculate_closest_station import calculate_closest_station
import utils.authentication.auth as auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def read_root(request: Request):
    return {"Hello":"World"}

#Pass the parameters for this function like so: http://127.0.0.1:8000/get_closest_stations/?latitude=20?longitude=20
@app.get('/get_closest_stations/')
def get_closest_station(latitude: float, longitude: float | None = None,
                        api_key: APIKey = Depends(auth.get_api_key)):
    return calculate_closest_station(latitude, longitude)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db), api_key: APIKey = Depends(auth.get_api_key),):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/add_stops_to_database/", response_model=schemas.Stop)
def create_stop(stop: schemas.StopCreate, db: Session = Depends(get_db), api_key: APIKey = Depends(auth.get_api_key),):
    return crud.create_stop(db=db, stop=stop)


@app.get("/users/", response_model=list[schemas.User],)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), api_key: APIKey = Depends(auth.get_api_key),):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db), api_key: APIKey = Depends(auth.get_api_key)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(
    user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db),
    api_key: APIKey = Depends(auth.get_api_key)
):
    return crud.create_user_item(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.Item])
def read_items(api_key: APIKey = Depends(auth.get_api_key), skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items

@app.get("/secure")
async def info(api_key: APIKey = Depends(auth.get_api_key)):
    return {
        "default variable": api_key
    }

# Have data collection 


# Have service for clients

# Have maintanence scheduled