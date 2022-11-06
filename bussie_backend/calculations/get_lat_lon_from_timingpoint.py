import json
  
# Opening JSON file
f = open('bussie_backend/calculations/timingpointdata.json')
  
# returns JSON object as 
# a dictionary
data = json.load(f)

# Iterating through the json
# list

def find_lat_lon(timingpoint):
    timingpoint = str(timingpoint)
    print("Trying: ", timingpoint)
    if timingpoint in data:
        longitude = data[timingpoint]['Stop']['Longitude']
        latitutde = data[timingpoint]['Stop']['Latitude']
        return {'Lat': latitutde, 'Lon':longitude}
    else:
        print("Not found")
  
# Closing file
f.close()
