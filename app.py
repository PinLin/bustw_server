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
        bus_routes = api.bus_route(maps[city], arg={'$select': 'RouteUID,RouteName,City,DepartureStopNameZh,DestinationStopNameZh'})
    except:
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
        except:
            result[-1]['city'] = city
        # 起站
        try:
            result[-1]['departureStopName'] = bus_route['DepartureStopNameZh']
        except:
            result[-1]['departureStopName'] = ''
        # 終站
        try:
            result[-1]['destinationStopName'] = bus_route['DestinationStopNameZh']
        except:
            result[-1]['destinationStopName'] = ''

    # 回傳
    return Response(json.dumps({'routes': result}, ensure_ascii=False), mimetype='application/json')

@app.route('/stop/<city>/<route>/')
def get_stop(city, route):
    # 讀取城市對應表
    with open(sys.path[0] + '/map.json', 'r') as f:
        maps = json.load(f)

    # 取得該城市符合條件的所有路線
    try:
        bus_stops = api.bus_stop(maps[city], route, arg={'$select': 'RouteUID,RouteName,City,Direction,SubRouteUID,SubRouteName,Stops'})
    except:
        bus_stops = []

    # 處理資料
    result = []
    for bus_stop in bus_stops:
        # 在 SubRouteUID 後方加入 Direction
        try:
            bus_stop['SubRouteUID'] += str(bus_stop['Direction'])
        except:
            pass

        # 記錄停靠站
        stop_list = []
        for stop in bus_stop['Stops']:
            # 不停靠的站不顯示
            if '不停靠' in stop['StopName']['Zh_tw']:
                continue
            # 停靠站名稱
            stop_list.append({
                'StopUID': stop['StopUID'],
                'StopName': stop['StopName']['Zh_tw'],
                'EstimateTime': None,
            })

        # 確認是否已經有該 UID 的資料
        exist = -1
        for i in range(len(result)):
            # 如果 UID 相同
            if result[i]['routeUID'] == bus_stop['RouteUID']:
                exist = i
                break

        # 如果已經存在該 UID 的資料
        if exist != -1:
            # 確認是否已經有該 subRouteUID 的資料
            repeat = False
            for i in range(len(result[exist]['subRoutes'])):
                # 如果 UID 相同
                if result[exist]['subRoutes'][i]['subRouteUID'] == bus_stop['SubRouteUID']:
                    repeat = True
                    break
            # 如果不存在該 subRouteUID 的資料
            if not repeat:
                # 新增子路線的資料
                result[exist]['subRoutes'].append({
                    # 子路線辨識碼
                    'subRouteUID': bus_stop['SubRouteUID'],
                    # 子路線名稱
                    'subRouteName': bus_stop['SubRouteName']['Zh_tw'],
                    # 停靠站列表
                    'stops': stop_list,
                })
        else:
            # 新增該路線的資料
            result.append({})
            # 路線辨識碼
            result[-1]['routeUID'] = bus_stop['RouteUID']
            # 路線名稱
            result[-1]['routeName'] = bus_stop['RouteName']['Zh_tw']
            # 城市
            try:
                result[-1]['city'] = bus_stop['City']
            except:
                result[-1]['city'] = city
            # 子路線
            result[-1]['subRoutes'] = [{
                # 子路線辨識碼
                'subRouteUID': bus_stop['SubRouteUID'],
                # 子路線名稱
                'subRouteName': bus_stop['SubRouteName']['Zh_tw'],
                # 停靠站列表
                'stops': stop_list,
            }]
            
    # 回傳
    return Response(json.dumps({'routes': result}, ensure_ascii=False), mimetype='application/json')

def main():
    app.run(port=65432)

if __name__ == '__main__':
    main()
