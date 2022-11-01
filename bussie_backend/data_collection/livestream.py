from gzip import GzipFile
from io import BytesIO
import string
from fastapi import Depends
import zmq
import xml.etree.ElementTree as ET

from bussie_backend.database import crud, models, schemas
from sqlalchemy.orm import Session
from ..database.database import SessionLocal, engine
import sqlite3


models.Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
            print("Updates Received:")
            # More comments
            # Gets the timestamp
            print('time', root[3].text)
            # Gets the operator of this transport
            print('operator: ', root[4][0][0].text)
            # Gets the line number
            print('line: ', root[4][0][1].text)
            print('X Coord: ', root[4][0][12].text)
            print('Y Coord: ', root[4][0][13].text)
            print(address)
            print("\n")

        except:
            print('\n\n############')
            print('ERROR in latest fetch')
            print('############\n')

    subscriber.close()
    context.term()
