# Data Collection
In this folder we keep all scripts and functions related to getting the information about the public transport into our database. 
The livestream of incoming messages for the public transport is ran from a separate docker container deployed to AWS alongside the main script. 
The idea is that since both the webserver and the scraper need to be on all the time they don't interfere with each other. We let the container service in AWS handle their concurrency. 

## Strategy
We listen to a ZeroMQ event stream over a TCP socket. The information is pushed to a Redis cache. 
Each item in the cache has a time to live of an hour, which is refreshed everytime a already known vehicle checks in. 


## Implementation
Each has a unique key in the cache consisting of the day + the journeynumber + the linenumber. This should be unique across the trip but as soon as the same vehicle switches to another route it becomes another entry. 