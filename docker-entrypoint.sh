#!/bin/bash

sed -i "s/{PTX_ID}/$PTX_ID/g" bustw_server/config.py
sed -i "s/{PTX_KEY}/$PTX_KEY/g" bustw_server/config.py

gunicorn -w 1 -k gthread --thread=8 -b 0.0.0.0:8000 run:app