from gzip import GzipFile
from io import BytesIO
import zmq
import xml.etree.ElementTree as ET

#Adding comment
context = zmq.Context()


subscriber = context.socket(zmq.SUB)
subscriber.connect("tcp://pubsub.besteffort.ndovloket.nl:7658")
subscriber.setsockopt(zmq.SUBSCRIBE, b"/RIG/KV6posinfo")
subscriber.setsockopt(zmq.SUBSCRIBE, b"/RIG/KV17cvlinfo")
subscriber.setsockopt(zmq.SUBSCRIBE, b"/RIG/NStreinpositiesInterface5")

# while True:
while True:
    multipart = subscriber.recv_multipart()
    address = multipart[0]
    try:
        # The data is sent gzipped compressed as bytes. This unpacks this and stores it in contents variable
        contents = GzipFile('','r',0,BytesIO(multipart[1])).read()
        root = ET.fromstring(contents)
        print("Update Received:")
        #Gets the timestamp
        print('time', root[3].text)
        #Gets the operator of this transport
        print('operator: ',root[4][0][0].text)
        #Gets the line number
        print('line: ', root[4][0][1].text)
        print('X Coord: ', root[4][0][12].text)
        print('Y Coord: ', root[4][0][13].text)
        print("\n")
        #print("transmission success")

    except:
        print('\n############')
        print('ERROR in latest fetch')
        print('############\n')


subscriber.close()
context.term()
