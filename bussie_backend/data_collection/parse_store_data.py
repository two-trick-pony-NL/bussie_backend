
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
import random


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

        #Creating new unique identifier of the vehicle which is: day + journey number + vehiclenumber
        unique_vehicle_identifier = str(root[4][0][2].text)+'_operator_'+str(root[4][0][0].text)+'__vehicle__'+ str(root[4][0][9].text)
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
            'locationsource': 'converted_from_RD_to_latlon',
            'punctuality': root[4][0][10].text,
            'since': root[4][0][11].text
            }
        rd.json().set(unique_vehicle_identifier, Path.root_path(), update)
        rd.expire(unique_vehicle_identifier, 120)
# In case no location is known we'll print that
    except:
        parse_unknown_structure(multipart)
        

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
            unique_vehicle_identifier = str(date.today())+'_operator_NS_vehicle_'+ str(root[i][1][0].text)
            update = {
                'type_vehicle': 'Train',
                'unique_vehicle_identifier': str(unique_vehicle_identifier),
                'dataownercode':'NS',
                'operatingday': str(date.today()),
                'timestamp': str(root[i][1][3].text),
                'source': "NS",
                'vehiclenumber': root[i][1][0].text,
                'Materieelvolgnummer': root[i][1][1].text,
                'since':root[i][1][3].text,
                'latitude': float(root[i][1][10].text),
                'longitude': float(root[i][1][9].text),
                'locationsource': 'exact_from_vehicle',
                'speed': root[i][1][12].text,
                'direction': root[i][1][13].text
                }
            rd.json().set(unique_vehicle_identifier, Path.root_path(), update)
            rd.expire(unique_vehicle_identifier, 10)
            i = i +1
# In case no location is known we'll print that
    except:
        parse_unknown_structure(multipart)
        
        
def parse_unknown_structure(multipart):
    # This method is slower because of the 2 for loops, however it catches all fields. 
    contents = GzipFile('', 'r', 0, BytesIO(multipart[1])).read()
    root = ET.fromstring(contents)
    try: 
        for i in root:
            items = len(root[4][0])
            vehicle_object = {'type_vehicle': 'BusOrTram'} # this is the empty object we'll parse to redis
            for j in range(0 , items): 
                if root[4][0][j].tag[38:] == 'rd-x': # if we have known location data we need to convert rd-xy to lat-lon
                    x = int(root[4][0][j].text)
                    y = int(root[4][0][j + 1].text)
                    latlon = convert(x, y)
                    vehicle_object['latitude'] = latlon[0]
                    vehicle_object['longitude'] = latlon[1]
                    vehicle_object['locationsource'] = 'converted_from_RD_to_latlon'
                if root[4][0][j].tag[38:] == 'userstopcode': # From the userstopcode we can derive a location too. 
                    vehicle_object['latitude'] = random.uniform(-90.0, 90.0)
                    vehicle_object['longitude'] = random.uniform(-90.0, 90.0)
                    vehicle_object['locationsource'] = 'random_until_we_can_derive_from_stop'
                    #vehicle_object['locationsource'] = 'approximated_from_busstop'
                else:
                    tag = root[4][0][j].tag[38:] #removing the first 38 characters of the tag
                    value = root[4][0][j].text  
                    vehicle_object[tag] = value
            unique_vehicle_identifier = str(root[4][0][2].text)+'_operator_'+str(root[4][0][0].text) +'_vehicle_'+ str(root[4][0][9].text)
            rd.json().set(unique_vehicle_identifier, Path.root_path(), vehicle_object)
            rd.expire(unique_vehicle_identifier, 120)
    except:
        try:
            for i in root:
                items = len(root[4][0])
                vehicle_object = {'type_vehicle': 'BusOrTram'} # this is the empty object we'll parse to redis
                for j in range(0 , items): 
                    if root[4][0][j].tag[38:] == 'rd-x': # if we have known location data we need to convert rd-xy to lat-lon
                        x = int(root[4][0][j].text)
                        y = int(root[4][0][j + 1].text)
                        latlon = convert(x, y)
                        vehicle_object['latitude'] = latlon[0]
                        vehicle_object['longitude'] = latlon[1]
                        vehicle_object['locationsource'] = 'converted_from_RD_to_latlon'
                    else:
                        tag = root[4][0][j].tag[38:] #removing the first 38 characters of the tag
                        value = root[4][0][j].text  
                        vehicle_object[tag] = value
                        vehicle_object['locationsource'] = 'no_information_available'
                unique_vehicle_identifier = "NO_KNOWN_LOCATION_"+str(root[4][0][2].text)+'_operator_'+str(root[4][0][0].text) +'_linenumber_'+ str(root[4][0][1].text)+'_journeynumber_'+ str(root[4][0][3].text)
                rd.json().set(unique_vehicle_identifier, Path.root_path(), vehicle_object)
                rd.expire(unique_vehicle_identifier, 120)
        except:
            pass