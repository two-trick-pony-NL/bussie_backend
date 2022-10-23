

# We should do a call here to the API like so: 
#  http://v0.ovapi.nl//stopareacode/utrneu
# However due to ratelimit issues I saved the output for Utrecht Neude to json
# Once we have proper access we can implement a get request
# Opening JSON file
f = open('neude.json')
data = json.load(f)

print(data)