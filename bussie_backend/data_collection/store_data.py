
from gzip import GzipFile
from io import BytesIO
from fastapi import Depends
import zmq
import xml.etree.ElementTree as ET
from ..calculations.Rijksdriekhoek_To_LatLon import convert
import redis
from redis.commands.json.path import Path

# Creating our redis server
rd = redis.Redis(host='localhost', port=6379, db=0)


def parse_bus(multipart):
    #address = multipart[0]
    try:
        # The data is sent gzipped
        # compressed as bytes
        # This unpacks this and stores it in contents variable
        contents = GzipFile('', 'r', 0, BytesIO(multipart[1])).read()
        #Contents gives you raw XML output. Root is a parsed version
        #print(contents)
        root = ET.fromstring(contents)
        x = int(root[4][0][12].text)
        y = int(root[4][0][13].text)
        latlon = convert(x, y)
        ##### NEW SECTION
        #Creating new unique identifier of the vehicle which is: day + journey number + vehiclenumber
        unique_vehicle_identifier = str(root[4][0][2].text)+'_journey_'+str(root[4][0][3].text) +'_line_'+ str(root[4][0][1].text)+'__vehicle__'+ str(root[4][0][9].text)
        update = {
            'type_vehicle': 'BusOrTram',
            'unique_vehicle_identifier': unique_vehicle_identifier,
            'dataownercode':root[4][0][0].text,
            'lineplanningnumber': root[4][0][1].text,
            'operatingday': root[4][0][2].text,
            'journeynumber': root[4][0][3].text,
            'reinforcementnumber': root[4][0][4].text,
            'userstopcode': root[4][0][5].text,
            'passagesequencenumber': root[4][0][6].text,
            'timestamp': root[4][0][7].text,
            'source': root[4][0][8].text,
            'vehiclenumber': root[4][0][9].text,
            'latitude': latlon[0],
            'longitude': latlon[1],
            'punctuality': root[4][0][10].text,
            'since': root[4][0][11].text,
            }
        rd.json().set(unique_vehicle_identifier, Path.root_path(), update)
        rd.expire(unique_vehicle_identifier, 120)
# In case no location is known we'll print that
    except Exception as e:
        """Nothing"""



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
            unique_vehicle_identifier = str(root[i][1][3].text)+'_journey_NONE_line_NONE__vehicle__'+ str(root[i][1][0].text)
            update = {
                'type_vehicle': 'Train',
                'unique_vehicle_identifier': unique_vehicle_identifier,
                'dataownercode':'NS',
                'lineplanningnumber': 'NULL',
                'operatingday': root[i][1][3].text,
                'journeynumber': "NULL",
                'reinforcementnumber': "NULL",
                'userstopcode': "NULL",
                'passagesequencenumber': "NULL",
                'timestamp': root[i][1][3].text,
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
        
