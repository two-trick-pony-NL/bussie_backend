# Infrastructure in AWS
This folder contains resources used by AWS to create and update our docker image at AWS Lightsail. There are 4 important files: 

1. gunicorn.sh --> This is our entrypoint starting the serverprocess in a container
2. deploymentconfig.json --> Telling the CI how we want the container to be deployed
   This sets ports and what image to use 
3. scriptpreferences.json --> Helps us filter in logging 
4. Publicendpoint.json --> Tells AWS what ports to expose and how to do healthchecks
5. capacity.py --> This script can be ran in order to scale up to more server capacity