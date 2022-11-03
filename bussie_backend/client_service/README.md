# Client Service
This folder will contains scripts and functions to support the client app asking for information. It's FastAPI

## Strategy - Polling
The app when live will poll the backend every few seconds for updates. The backend gets these updates from the database. This cache is filled with information from the livestream script folder. 

# Caching
We use caching in several places. First we store information about each vehicle for 1 hour after that it is removed from the database. We cache where each vehicle is located and have that expire every 5 seconds. This should ensure that with high usage most users get data that is calculated once but is still up to date very 5 seconds. 
Further improvement could be to split concerns so calculating where very vehicle is can be done in a separate process and cached. Removing the calculation from the endpoint. 