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

@app.route('/info/<city>/')
def get_info(city):
    # 讀取城市對應表
    with open(sys.path[0] + '/map.json', 'r') as f:
        maps = json.load(f)

    # 取得該城市符合條件的所有路線
    try:
        routes = api.bus_route(maps[city])
    except:
        routes = []

    # 處理資料
    data = []
    for route in routes:
        # 只留下需要的資料
        data.append({
            # 路線辨識碼
            'routeUID': route['RouteUID'],
            # 路線名稱
            'routeName': route['RouteName']['Zh_tw'],
            # 城市
            'city': city,
            # 起站
            'departureStopName': route['DepartureStopNameZh'],
            # 終站
            'destinationStopName': route['DestinationStopNameZh'],
        })

    # 回傳
    return Response(json.dumps({'routes': data}, ensure_ascii=False), mimetype='application/json')

@app.route('/stop/<city>/<route>/')
def get_stop(city, route):
    # 讀取城市對應表
    with open(sys.path[0] + '/map.json', 'r') as f:
        maps = json.load(f)

    # 取得該城市符合條件的所有路線
    try:
        routes = api.bus_stop(maps[city], route)
    except:
        routes = []

    # 處理資料
    data = []
    for route in routes:
        # 記錄停靠站
        stops = []
        for stop in route['Stops']:
            # 不停靠的站不顯示
            if '不停靠' in stop['StopName']['Zh_tw']:
                continue
            # 停靠站名稱
            stops.append(stop['StopName']['Zh_tw'])

        # 在 SubRouteUID 後方加入 Direction
        route['SubRouteUID'] += str(route['Direction'] if 'Direction' in route else '')

        # 確認是否已經有該 UID 的資料
        exist = -1
        for i in range(len(data)):
            # 如果 UID 相同
            if data[i]['routeUID'] == route['RouteUID']:
                exist = i
                break

        # 如果已經存在該 UID 的資料
        if exist != -1:
            # 確認是否已經有該 subRouteUID 的資料
            repeat = False
            for i in range(len(data[exist]['subRoutes'])):
                # 如果 UID 相同
                if data[exist]['subRoutes'][i]['subRouteUID'] == route['SubRouteUID']:
                    repeat = True
                    break
            # 如果不存在該 subRouteUID 的資料
            if not repeat:
                # 新增子路線的資料
                data[exist]['subRoutes'].append({
                    # 子路線辨識碼
                    'subRouteUID': route['SubRouteUID'],
                    # 子路線名稱
                    'subRouteName': route['SubRouteName']['Zh_tw'],
                    # 停靠站列表
                    'stops': stops,
                })
        else:
            # 新增該路線的資料
            data.append({
                # 路線辨識碼
                'routeUID': route['RouteUID'],
                # 路線名稱
                'routeName': route['RouteName']['Zh_tw'],
                # 城市
                'city': city,
                # 子路線
                'subRoutes': [{
                    # 子路線辨識碼
                    'subRouteUID': route['SubRouteUID'],
                    # 子路線名稱
                    'subRouteName': route['SubRouteName']['Zh_tw'],
                    # 停靠站列表
                    'stops': stops,
                }],
            })
            
    # 回傳
    return Response(json.dumps({'routes': data}, ensure_ascii=False), mimetype='application/json')

def main():
    app.run(port=65432)

if __name__ == '__main__':
    main()
