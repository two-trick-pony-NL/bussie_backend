import xml.etree.ElementTree as ET
from .Rijksdriekhoek_To_LatLon import convert
from termcolor import colored


print(colored('🧮 Calculating lat/lon for each station', 'green'), colored('-- This might take a minute', 'white'))
# Passing the path of the
# xml document to enable the
# parsing process
tree = ET.parse('bussie_backend/calculations/stops.xml')
 
# getting the parent tag of
# the xml document
root = tree.getroot()
 
# This is a in memory dictionairy with all data on stops. 
stops = {}

for item in root[0]: #by selecting 0 we only look at Stopplaces, other options are "places" and 'dataowners'
    stop = {}
    try:
        stop['stopplace'] = item[0].text
        stop['stopplacecode'] = item[2].text
        stop['stopplacetype'] = item[3].text
        stop['stopplacename'] = item[4][1].text
        stop['stopplacetown'] = item[4][2].text
        stop['stopplacestreetname'] = item[4][4].text
        stop['stopplacestatus'] = item[5][1].text
        x = int(item[7][0][6][1].text)
        y = int(item[7][0][6][2].text)
        latlon = convert(x, y)
        stop['latitude'] = latlon[0]
        stop['longitude'] = latlon[1]
        stops[item[2].text[5:]] = stop
    except Exception as e:
        try: #Trainstations have their latlon on a different place
            stop['stopplace'] = item[0].text
            stop['stopplacecode'] = item[2].text
            stop['stopplacetype'] = item[3].text
            x = int(item[9][2].text)
            y = int(item[9][3].text)
            latlon = convert(x, y)
            stop['latitude'] = latlon[0]
            stop['longitude'] = latlon[1]
            stops[item[2].text[5:]] = stop
        except Exception as a:
            """stopplace = item[0].text
            stopplacecode = item[2].text
            stopplacetype = item[3].text
            print(stopplace, stopplacecode, stopplacetype)
            print(a)"""
print(colored('🎉 Calculations done', 'green'), colored('-- Stored the results in memory', 'white'))


def user_stop_location(userstopcode):
    try:
        latitude = stops[str(userstopcode)]['latitude']
        longitude = stops[str(userstopcode)]['longitude']
        return latitude, longitude
    except:
        return 1, 1

def user_stop_data(userstopcode):
    return stops[str(userstopcode)]
