
from gzip import GzipFile
from io import BytesIO
from fastapi import Depends
import zmq
import xml.etree.ElementTree as ET
from ..calculations.Rijksdriekhoek_To_LatLon import convert
from ..calculations.get_lat_lon_from_timingpoint import find_lat_lon
import redis
from redis.commands.json.path import Path
from datetime import date
from termcolor import colored


# Creating our redis server
rd = redis.Redis(host='localhost', port=6379, db=0)

def parse_data(multipart):
    contents = GzipFile('', 'r', 0, BytesIO(multipart[1])).read()
    root = ET.fromstring(contents)
    try: 
        for i in root:
            if root.tag[70:] == 'ArrayOfTreinLocation':
                parse_train(multipart)
                pass
            else:
                items = len(root[4][0])
                vehicle_object = {'type_vehicle': 'BusOrTram'} # this is the empty object we'll parse to redis
                for j in range(0 , items): 
                    if root[4][0][j].tag[38:] == 'rd-x': # if we have known location data we need to convert rd-xy to lat-lon
                        x = int(root[4][0][j].text)
                        y = int(root[4][0][j + 1].text)
                        latlon = convert(x, y)
                        vehicle_object['latitude'] = latlon[0]
                        vehicle_object['longitude'] = latlon[1]
                    if root[4][0][j].tag[38:] == 'rd-y':
                        pass # We don't want the rd-y label in our dataset
                    else:
                        tag = root[4][0][j].tag[38:] #removing the first 38 characters of the tag
                        value = root[4][0][j].text  
                        vehicle_object[tag] = value
                unique_vehicle_identifier = str(root[4][0][2].text)+'_journey_'+str(root[4][0][3].text) +'_line_'+ str(root[4][0][1].text)
                rd.json().set(unique_vehicle_identifier, Path.root_path(), vehicle_object)
                rd.expire(unique_vehicle_identifier, 120)
    except Exception as e:
        print(e)
        

def parse_train(multipart):
    try:
        # The data is sent gzipped
        # compressed as bytes
        # This unpacks this and stores it in contents variable
        contents = GzipFile('', 'r', 0, BytesIO(multipart[1])).read()
        root = ET.fromstring(contents)
        # Using I as iterator as we don't need to know how big the contents are, as long as we look for the next one on each pass. 
        i = 0
        for _ in root:
            #Creating unique name
            unique_vehicle_identifier = str(date.today())+'_journey_NONE_line_NONE__vehicle__'+ str(root[i][1][0].text)
            update = {
                'type_vehicle': 'Train',
                'unique_vehicle_identifier': str(unique_vehicle_identifier),
                'dataownercode':'NS',
                'lineplanningnumber': 'NULL',
                'operatingday': str(date.today()),
                'journeynumber': "NULL",
                'reinforcementnumber': "NULL",
                'userstopcode': "NULL",
                'passagesequencenumber': "NULL",
                'timestamp': str(root[i][1][3].text),
                'source': "NS",
                'vehiclenumber': root[i][1][0].text,
                'latitude': root[i][1][10].text,
                'longitude': root[i][1][9].text,
                'punctuality': "NULL",
                'since': "NULL",
                'speed': root[i][1][12].text
                }
            rd.json().set(unique_vehicle_identifier, Path.root_path(), update)
            rd.expire(unique_vehicle_identifier, 10)
            i = i +1

# In case no location is known we'll print that
    except:
        """Do nothing"""
        
