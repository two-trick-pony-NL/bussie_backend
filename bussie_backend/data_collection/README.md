# Data Collection
In this folder we keep all scripts and functions related to getting the information about the public transport into our database. 
The livestream of incoming messages for the public transport is ran from a separate docker container deployed to AWS alongside the main script. 
The idea is that since both the webserver and the scraper need to be on all the time they don't interfere with each other. We let the container service in AWS handle their concurrency. 

## Strategy
Ideally we listen to an event stream over a TCP socket updating our database live as the information comes in. The files in CLIENT_SERVER are then concerned with getting that data from the database back to the client. 

## Implementation

WRITE UP HOW THIS WILL WORK