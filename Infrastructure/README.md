# Infrastructure in AWS
This folder contains resources used by AWS to create and update our docker image at AWS Lightsail. There are 4 important files: 

1. gunicorn.sh --> This is our entrypoint starting the serverprocess in a container. We however run uvicorn from the python script itself. 
2. deploymentconfig.json --> Telling the CI how we want our backend container to be deployed
   This sets ports and what image to use. It also specifies a Redis container to be started. This is used for storing the current vehicles in a cache. 
3. scriptpreferences.json --> Helps us filter in logging 
4. Publicendpoint.json --> Tells AWS what ports to expose and how to do healthchecks
5. capacity.py --> This script can be ran in order to scale up to more server capacity from the command line