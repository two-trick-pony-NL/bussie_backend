# Bussie -- komt zo
Bussie helps you get from A to B by sharing the live location of your next bus, tram or train!
<img width="1402" alt="Screenshot 2022-11-06 at 19 18 26" src="https://user-images.githubusercontent.com/71013416/200188012-9c79d78a-bc32-4392-94b6-82e4d0010890.png">


# Goal
The idea is that while walking to the platform for a trip with the bus, you can see where your bus is right now and as a result decide whether you want to grab a cup of coffee or that the bus is too close and you better hurry

# Technology
The Bussie backend runs on FastAPI with redis and SQLite on AWS Lightsail containers. CI is implemented to do deployments

# Installation
For dev: 
- Run a standard redis docker container on it's standard port and then run main.py to start the server. From localhost/docs you should be able to access the SWAGGER documentation

For prod: 
You'll need 2 requirements:
- simply add your AWS information to the Github action secrets
- Make sure you have a container service named bussie in AWS lighstail 
From there the github action should use your AWS credentials to launch the application and reate another Redis container under your account and provide you with an endpoint. 

# Companion app
Checkout the Bussie app here: https://github.com/two-trick-pony-NL/bussie_app 
And check out our analytics here: https://two-trick-pony-nl-bussie-analytics-dashboard-szt85z.streamlit.app/
