#!/bin/bash

sed -i "s/{PTX_ID}/$PTX_ID/g" config.py
sed -i "s/{PTX_KEY}/$PTX_KEY/g" config.py

poetry run gunicorn -w 1 -k gthread --thread=8 -b 0.0.0.0:8000 app:app
