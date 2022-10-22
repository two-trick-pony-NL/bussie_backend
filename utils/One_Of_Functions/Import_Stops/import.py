import json
import requests

#This function reads the json file also in this folder which I got here: http://v0.ovapi.nl/stopareacode
#It adds all separate stations to our database

# api-endpoint
URL = "http://127.0.0.1:8000/stops/"
HEADERS = {"Content-type": "application/json"}
  
# Opening JSON file
f = open('stations.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)

# Iterating through the json
# list
print(len(data))
for i in data:
    TimingPointTown = data[i]['TimingPointTown']
    TimingPointName = data[i]['TimingPointName']
    StopAreaCode = data[i]['StopAreaCode']
    Longitude = float(data[i]['Longitude'])
    Latitude = float(data[i]['Latitude'])
    print(StopAreaCode)
    print(Longitude)
    print(Latitude)

    new_stop = {'TimingPointName':TimingPointName,
        'latitude':float(Latitude),
        'longitude':float(Longitude),
        'TimingPointTown':TimingPointTown,
        'StopAreaCode':StopAreaCode}

    r = requests.post(url = URL, json = new_stop, headers = HEADERS)
    print(r.text)
    
  
# Closing file
f.close()