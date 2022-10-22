from fastapi import FastAPI, File, Request
from fastapistats import Stats
from datetime import datetime

app = FastAPI()
update = Stats.update_stats


@app.get('/')
@update(name='Homepage') 
def read_root(request: Request):
    return {"Hello":"World"}

