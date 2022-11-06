import requests
import json
url = 'http://v0.ovapi.nl/tpc/'



resp = requests.get(url=url)
data = resp.json() # Check the JSON Response Content documentation below

infolist = {}

string = ''
h = 0 
print("Starting Loop")
for i in data:
    try: 
        string = string + ','+ i 
        h + 1
        if h % 200:
            response = requests.get(url=url+string)
            json_object = json.dumps(response, indent=4)
            

            
        
    except:
        print("OOP")




# Writing to sample.json
with open("tpc.json", "w") as outfile:
    outfile.write(json_object)


