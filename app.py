#!/usr/bin/env python3

from flask import Flask, request, Response
from pprint import pprint
import sys
import json

from ptx import PTX

# 初始化
api = PTX()
app = Flask(__name__)

@app.route('/')
def get_intro():
    return '<meta http-equiv="refresh" content="0; url=https://gitea.ntut.com.tw/PinLin/bustw_server">'

@app.route('/info/<city>')
def get_info(city):
    # 讀取城市對應表
    with open(sys.path[0] + '/city_map.json', 'r') as f:
        city_map = json.load(f)
    # 取得該城市符合條件的所有路線
    try:
        routes = api.bus_routes(city_map[city])
    except KeyError:
        routes = {}
    # 處理資料
    data = {}
    for route in routes: 
        # 只留下需要的
        data[route['RouteUID']] = {
            # 路線名稱
            'routeName': route['RouteName']['Zh_tw'],
            # 起站
            'departureStopName': route['DepartureStopNameZh'],
            # 終站
            'destinationStopName': route['DestinationStopNameZh'],
            # 城市
            'city': city,
        }
        # 子路線
        subroutes = {}
        for subroute in route['SubRoutes']:
            newUID = subroute['SubRouteUID'] + str(subroute['Direction'] if 'Direction' in subroute else '')
            subroutes[newUID] = {
                # 子路線名稱
                'subRouteName': subroute['SubRouteName']['Zh_tw'],
            }
        data[route['RouteUID']]['subRoutes'] = subroutes
    # 回傳
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

@app.route('/stop/<city>/<route>')
def get_stop(city, route):
    # 讀取城市對應表
    with open(sys.path[0] + '/city_map.json', 'r') as f:
        city_map = json.load(f)
    # 取得該城市符合條件的所有路線
    try:
        routes = api.bus_stops(city_map[city], route)
    except KeyError:
        routes = {}
    # 處理資料
    data = {}
    for route in routes:
        # 路線名稱
        if not route['RouteUID'] in data:
            data[route['RouteUID']] = {}
        data[route['RouteUID']]['routeName'] = route['RouteName']['Zh_tw']
        # 城市
        data[route['RouteUID']]['city'] = city
        # 子路線
        if not 'SubRoutes' in data[route['RouteUID']]:
            data[route['RouteUID']]['subRoutes'] = {}
        newUID = route['SubRouteUID'] + str(route['Direction'] if 'Direction' in route else '')
        data[route['RouteUID']]['subRoutes'][newUID] = {
            # 子路線名稱
            'subRouteName': route['SubRouteName']['Zh_tw'],
        }
        # 停靠站
        stops = []
        for stop in route['Stops']:
            # 不停靠的站不顯示
            if '不停靠' in stop['StopName']['Zh_tw']:
                continue
            # 停靠站名稱
            stops.append(stop['StopName']['Zh_tw'])
        data[route['RouteUID']]['subRoutes'][newUID]['stops'] = stops
    # 回傳
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

def main():
    app.run(port=65432)

if __name__ == '__main__':
    main()
