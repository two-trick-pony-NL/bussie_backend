from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from bussie_backend.database import crud, models, schemas
from bussie_backend.database.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def read_root(request: Request):
    return {"Hello":"World"}

### Have data collection 


### Have service for clients