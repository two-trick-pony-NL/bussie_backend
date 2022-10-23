from requests.auth import HTTPBasicAuth
import requests

url = 'http://0.0.0.0/get_closest_stations/?latitude=1.0&longitude=1.0'
headers = {'Accept': 'application/json', 'access_token':'PETER'}

req = requests.get(url, headers=headers)
print(req.text)