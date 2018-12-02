#!/bin/bash

rm bustw_server/config.py
echo "PTX_ID = \"$PTX_ID\"" >> bustw_server/config.py
echo "PTX_KEY = \"$PTX_KEY\"" >> bustw_server/config.py

gunicorn -w 1 -k gthread --thread=8 -b 0.0.0.0:8000 run:app