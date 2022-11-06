from gzip import GzipFile
from io import BytesIO
from fastapi import Depends
import zmq
import xml.etree.ElementTree as ET
from ..calculations.Rijksdriekhoek_To_LatLon import convert
from redis.commands.json.path import Path
from .store_data import parse_bus, parse_train




"""
See documentation on how to use the live feed here: http://data.ndovloket.nl/REALTIME.TXT 
With a python example: http://htmwiki.nl/#!hackathon/realtime.md 
"""

def worker():
    # Defining ZMQ
    context = zmq.Context()
    #Defining the streams we'll be listening on
    # Bison is most buses
    subscriber = context.socket(zmq.SUB)
    subscriber.connect("tcp://pubsub.besteffort.ndovloket.nl:7658")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/RIG/KV6posinfo")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/ARR/KV6posinfo")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/CXX/KV6posinfo")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/GVB/KV6posinfo")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/EBS/KV6posinfo")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/OPENOV/KV6posinfo")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/QBUZZ/KV6posinfo")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/DITP/KV6posinfo")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/SYNTUS/KV6posinfo")
    # Infoplus contains all NS train info
    subscriber.connect("tcp://pubsub.besteffort.ndovloket.nl:7664")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/RIG/NStreinpositiesInterface5")
    
    #bison.setsockopt(zmq.SUBSCRIBE, b"/RIG/KV17cvlinfo")

    while True:
        data = subscriber.recv_multipart()
        parse_bus(data)
        parse_train(data)
