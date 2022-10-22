# Bussie Backend
This folder contains the major functions used to run the bussie service. I split out different services over different folders to keep an organised codebase. 

In this folder you'll find these important partitions: 
- calculations --> General compute functions that can be called in other files
- client_service --> Facilitates communication with the bussie app users
- data_collection --> Pulls the data we need from the external register and stores it in the database
- database --> all files and functions and models for the database