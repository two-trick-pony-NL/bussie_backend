# Calculations
This folder contains files and functions related to general computing. This allows us to store specific functions here keeping the other control/ communications scripts concise. 

## Table of content
#### calculate closest station
This set of functions takes a lat-lon position and return the closest known station relative to that location. 
It is used to be able what vehicles are and routes are relavant to the user 

#### Rijksdriekhoek to latlon
The locationdata of each vehicle comes in the format of Rijksdriehoek (https://nl.wikipedia.org/wiki/Rijksdriehoeksco%C3%B6rdinaten) 
In order to use it with other location data we need standardisation. As a result we have a set of functions that allows us to convert this rijksdriehoek location into a lat/lon. 

#### calculate vehicles on route to stop 
These set of functions aim to calculate what vehicles have a stop at the station closest to the user. 
This calculation is yet to be implemented. 