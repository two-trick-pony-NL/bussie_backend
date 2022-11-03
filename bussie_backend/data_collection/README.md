# Data Collection
In this folder we keep all scripts and functions related to getting the information about the public transport into our cache in redis. 
The livestream runs in another process alongside FastAPI both run in 1 container. In another container we run a redis cache used to save all incoming data.
This allows for fast access to the data and also allows us to cache ready made responses for better scaling. 

## Strategy
We listen to a ZeroMQ event stream over a TCP socket. The information is pushed to a Redis cache. 
Each item in the cache has a time to live of an hour, which is reset everytime a already known vehicle checks in. This prevent vehicles from completing their route and not disappearing from the database. 


## Implementation
Each vehicle has a unique key in the cache consisting of the day + the journeynumber + the linenumber. This should be unique across the trip but as soon as the same vehicle switches to another route it becomes another entry. The cache gets updated from a python implementation of redis. 
In the development server you can run a Redis docker image locally if you want the main script to work. 