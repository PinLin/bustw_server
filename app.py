#!/usr/bin/env python3

from flask import Flask, request, Response
from pprint import pprint
import sys
import json

from ptx import PTX

# 初始化
api = PTX()
app = Flask(__name__)

@app.route('/info/<city>')
def get_info(city):
    # 讀取城市對應表
    with open(sys.path[0] + '/city_map.json', 'r') as f:
        city_map = json.load(f)
    # 取得該城市符合條件的所有路線
    routes = api.bus_routes(city_map[city])
    # 處理資料
    data = {}
    for route in routes: 
        # 只留下需要的
        data[route['RouteUID']] = {
            # 路線名稱
            'RouteName': route['RouteName']['Zh_tw'],
            # 起站
            'DepartureStopName': route['DepartureStopNameZh'],
            # 終站
            'DestinationStopName': route['DestinationStopNameZh'],
            # 城市
            'City': city,
        }
        # 子路線
        subroutes = {}
        for subroute in route['SubRoutes']:
            newUID = subroute['SubRouteUID'] + str(subroute['Direction'] if 'Direction' in subroute else '')
            subroutes[newUID] = {
                # 子路線名稱
                'SubRouteName': subroute['SubRouteName']['Zh_tw'],
            }
        data[route['RouteUID']]['SubRoutes'] = subroutes
    # 回傳
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

@app.route('/stop/<city>/<name>')
def get_stop(city, name):
    # 讀取城市對應表
    with open(sys.path[0] + '/city_map.json', 'r') as f:
        city_map = json.load(f)
    # 取得該城市符合條件的所有路線
    routes = api.bus_stops(city_map[city], name)
    # 處理資料
    data = {}
    for route in routes:
        # 路線名稱
        if not route['RouteUID'] in data:
            data[route['RouteUID']] = {}
        data[route['RouteUID']]['RouteName'] = route['RouteName']['Zh_tw']
        # 城市
        data[route['RouteUID']]['City'] = city
        # 子路線
        if not 'SubRoutes' in data[route['RouteUID']]:
            data[route['RouteUID']]['SubRoutes'] = {}
        newUID = route['SubRouteUID'] + str(route['Direction'] if 'Direction' in route else '')
        data[route['RouteUID']]['SubRoutes'][newUID] = {
            # 子路線名稱
            'SubRouteName': route['SubRouteName']['Zh_tw'],
        }
        # 停靠站
        stops = []
        for stop in route['Stops']:
            # 不停靠的站不顯示
            if '不停靠' in stop['StopName']['Zh_tw']:
                continue
            # 停靠站名稱
            stops.append(stop['StopName']['Zh_tw'])
        data[route['RouteUID']]['SubRoutes'][newUID]['Stops'] = stops
    # 回傳
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

def main():
    app.run("0.0.0.0", 65432, debug=True)

if __name__ == '__main__':
    main()
