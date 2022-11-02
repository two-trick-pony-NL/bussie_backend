from gzip import GzipFile
from io import BytesIO
import string
from fastapi import Depends
import zmq
import xml.etree.ElementTree as ET
from ..calculations.Rijksdriekhoek_To_LatLon import convert
import json


"""
See documentation on how to use the live feed here: http://data.ndovloket.nl/REALTIME.TXT 
With a python example: http://htmwiki.nl/#!hackathon/realtime.md 
"""

payload = {}

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
            root = ET.fromstring(contents)
            """print("\n\n##### New GPS Location Received #####")
            # More comments
            # Gets the timestamp
            print('time', root[3].text)
            # Gets the operator of this transport
            print('operator: ', root[4][0][0].text)
            # Gets the line number
            print('line: ', root[4][0][1].text)
            
            # Here we convert from RDS (Rijksdriehoek) coordinates we receive
            # To a lat/lon that we can use in the frontend
            test = convert(x, y)
            print('X Coord: ', test[0])
            print('Y Coord: ', test[1])
            print("Source: ", address)
            print("\n\n##### ##### ##### ##### #####")
            print("\n")"""
            x = int(root[4][0][12].text)
            y = int(root[4][0][13].text)
            latlon = convert(x, y)
            lat = latlon[0]
            lon = latlon[1]
            line = {'linenumber': root[4][0][1].text, 'longitude': lat, 'latitude':lon}
            payload[root[4][0][1].text] = line
            #print(payload)
            # Serializing json
            json_object = json.dumps(payload, indent=4)

            # Writing to sample.json
            with open("vehiclelocations.json", "w") as outfile:
                outfile.write(json_object)

        # In case no location is known we'll print that
        except:
            """
            print('X Coord: null')
            print('Y Coord: null')
            print("Source: ", address)
            print("\n\n##### ##### ##### ##### #####")
            print("\n")"""

    subscriber.close()
    context.term()

def send_all_location():
    return payload
