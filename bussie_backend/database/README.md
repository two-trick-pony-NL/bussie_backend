# Database
This folder contains all database related files. Most importantly the database models are described here but it also contains standard CRUD functions. Lastly we installed Alembic so that we can do migrations. 

## How to do DB migrations
Fill the blanks

## Rationale for using a SQLite DB
We pickec a SQLite database since it's the easiest to set up and lowest cost. Initially we don't care that the database can be destroyed by containers crashing or getting out of sync. Because the routes we track will be updated on a minute or even second basis. So as soon as a new servers spins up it will start tracking using it's own database. 