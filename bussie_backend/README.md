# Bussie Backend
This folder contains all the code used to operate the application. 

## Basic tech used
Bussie consists of a FastAPI backend with Redis Cache and a SQLite database. 
Hosting is done on AWS lightsail, for that see the infrastructure folder. 

## Storage and cache
As a storage medium this application uses a redis cache (In a separate container see infrastructure/deploymentconfig.json for context) for fast reading and writing. Persistant storage is handled in a SQLite

# in this folder
In this folder you'll find these important partitions: 
- calculations --> complex compute functions that can be called in other files. This keeps scripts and endpoints concise while also being able to do complex math. 
- client_service --> Facilitates communication with the bussie app users. So contains all endpoints and API's
- data_collection --> Script for retrieving the data we need from the external register and stores it in the cache
- database --> all files and functions and models for the database

n.b. the redis cache is a standard implementation of a docker container so that runs on its own without config or specific code. 