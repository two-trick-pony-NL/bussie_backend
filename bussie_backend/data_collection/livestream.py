import zmq
from .parse_store_data import parse_bus, parse_train
from termcolor import colored




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
    subscriber.connect("tcp://pubsub.ndovloket.nl:7658")
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
    subscriber.connect("tcp://pubsub.ndovloket.nl:7664")
    subscriber.setsockopt(zmq.SUBSCRIBE, b"/RIG/NStreinpositiesInterface5")
    
    #bison.setsockopt(zmq.SUBSCRIBE, b"/RIG/KV17cvlinfo")
    counter = 0 
    while True:
        data = subscriber.recv_multipart()
        # These 2 functions parse the data coming in as the XML formats differ ever so slightly
        parse_bus(data)
        parse_train(data)
        if counter == 0:
            print(colored('📬 First data received', 'green'), colored('-- Storing in Redis', 'white'))
        # Simple counter that prints every 1000 entries so we'll keep a heartbeat in the logs. 
        counter = counter + 1
        if counter % 100 == 0:
            print(colored('📝 Data received', 'green'), colored('-- '+str(counter)+' datapoints processed', 'white'))
