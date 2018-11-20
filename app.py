#!/usr/bin/env python3

import sys
import json

from flask import Flask, request, redirect, Response, jsonify
from ptx_api import PTX

from city import city_api
from info import info_api
from stop import stop_api
import config

# 初始化 Flask
app = Flask(__name__)
app.register_blueprint(city_api)
app.register_blueprint(info_api)
app.register_blueprint(stop_api)

# 初始化 PTX
ptx = PTX(config.API_ID, config.API_KEY)

# 載入縣市名稱對照表
with open(sys.path[0] + '/city.json', 'r') as f:
    taiwan = json.load(f)
    # 只保留 API 名稱
    for city in taiwan:
        taiwan[city] = taiwan[city]['code']

data = {'taiwan': taiwan}


@app.route('/v1/', strict_slashes=False)
def welcome():
    return jsonify({'message': "Welcome to bustw_server!"})


def main():
    app.run(debug=True, threaded=True)


if __name__ == '__main__':
    main()
