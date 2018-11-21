#!/usr/bin/env python3

import sys
import json

from flask import Blueprint, jsonify
from ptx_api import PTX

from .config import API_ID, API_KEY

# 載入縣市資料對照表
with open(sys.path[0] + '/bustw_server/taiwan.json', 'r') as f:
    data = json.load(f)

# 取得縣市代碼對照表
cities = {}
for key in data:
    cities[key] = data[key]['code']

# 初始化 PTX
ptx = PTX(API_ID, API_KEY)

# 初始化 info 藍圖
info_api = Blueprint('info', __name__)


@info_api.route('/v1/info/<city>/', strict_slashes=False)
def get_routes_info(city):
    """取得該城市符合條件的所有路線"""

    try:
        # 從 PTX 取得資料
        bus_routes = ptx.get("/v2/Bus/Route/{city}".format(city=cities[city]),
                             params={'$select': 'RouteUID,RouteName,City,DepartureStopNameZh,DestinationStopNameZh'})
    except KeyError:
        bus_routes = []

    # 處理資料
    result = []
    for bus_route in bus_routes:
        # 只留下需要的資料
        result.append({})
        # 路線辨識碼
        result[-1]['routeUID'] = bus_route['RouteUID']
        # 路線名稱
        result[-1]['routeName'] = bus_route['RouteName']['Zh_tw']
        # 城市
        try:
            result[-1]['city'] = bus_route['City']
        except KeyError:
            result[-1]['city'] = city
        # 起站
        try:
            result[-1]['departureStopName'] = bus_route['DepartureStopNameZh']
        except KeyError:
            result[-1]['departureStopName'] = ''
        # 終站
        try:
            result[-1]['destinationStopName'] = bus_route['DestinationStopNameZh']
        except KeyError:
            result[-1]['destinationStopName'] = ''

    # 回傳
    return jsonify({'routes': result})
