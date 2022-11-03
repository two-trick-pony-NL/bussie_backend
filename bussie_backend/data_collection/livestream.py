from gzip import GzipFile
from io import BytesIO
import string
from fastapi import Depends
import zmq
import xml.etree.ElementTree as ET
from ..calculations.Rijksdriekhoek_To_LatLon import convert
import json
import redis
from redis.commands.json.path import Path




"""
See documentation on how to use the live feed here: http://data.ndovloket.nl/REALTIME.TXT 
With a python example: http://htmwiki.nl/#!hackathon/realtime.md 
"""

payload = {}

# Creating our redis server
rd = redis.Redis(host='localhost', port=6379, db=0)

def worker():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://pubsub.besteffort.ndovloket.nl:7658")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/RIG/KV6posinfo")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/CXX/KV6posinfo")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/GVB/KV6posinfo")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/EBS/KV6posinfo")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/OPENOV/KV6posinfo")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/QBUZZ/KV6posinfo")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/SYNTUS/KV6posinfo")
    #subscriber.setsockopt(zmq.SUBSCRIBE, b"/RIG/KV17cvlinfo")
    #subscriber.setsockopt(zmq.SUBSCRIBE, b"/RIG/NStreinpositiesInterface5")

    while True:
        multipart = subscriber.recv_multipart()
        address = multipart[0]
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
            unique_vehicle_identifier = str(root[4][0][2].text)+'_journey_'+str(root[4][0][3].text) +'_line_'+ str(root[4][0][1].text)
            update = {
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
            rd.expire(unique_vehicle_identifier, 3600)
    # In case no location is known we'll print that
        except:
            """Do nothing"""
    subscriber.close()
    context.term()

def send_all_location():
    return payload
