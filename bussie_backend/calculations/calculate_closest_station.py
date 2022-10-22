from sqlalchemy.orm import Session
from bussie_backend.database import crud, models, schemas
from bussie_backend.database.database import SessionLocal, engine
import json
import sqlite3

from math import cos, asin, sqrt


#Haversine function to calculate the distance between points on a GLOBE
def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2
    return 12742 * asin(sqrt(hav))

def closest(data, v):
    return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))

# This function takes the lat/lon from a app user and returns the closest station we have in our database
def calculate_closest_station(lat, lon):
    #Get Coordinates of user store in v
    user_location = {'lat': lat, 'lon': lon}
    # Create a SQL connection to our SQLite database
    con = sqlite3.connect("bussie_backend/database/bussie.db")
    cur = con.cursor()

    stations_in_memory = []
    for row in cur.execute('SELECT * FROM stops;'):
        TimingPointName = row[1]
        StopAreaCode = row[4]
        Latitude = row[2]
        Longitude = row[3]
        my_dict = {'StopAreaCode': StopAreaCode, 'TimingPointName': TimingPointName, 'lon': Longitude, 'lat': Latitude}
        stations_in_memory.append(my_dict)
    con.close()
    return closest(stations_in_memory, user_location)

