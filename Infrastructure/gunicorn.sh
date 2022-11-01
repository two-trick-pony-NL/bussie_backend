#!/bin/sh
uvicorn main:app

#gunicorn main:app -w 4 --threads 2 -b 0.0.0.0:80
#gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
