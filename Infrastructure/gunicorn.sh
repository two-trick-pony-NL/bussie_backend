#!/bin/sh
python3 main.py
#gunicorn main:app -w 4 --threads 2 -b 0.0.0.0:80