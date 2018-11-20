#!/usr/bin/env python3

import sys
import json

from flask import Flask, request, redirect, Response, jsonify
from ptx_api import PTX

from city import city_api
import config

# 初始化 Flask
app = Flask(__name__)
app.register_blueprint(city_api)

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


@app.route('/v1/info/<city>/', strict_slashes=False)
def get_info(city):
    """取得該城市符合條件的所有路線"""

    try:
        # 從 PTX 取得資料
        bus_routes = ptx.get("/v2/Bus/Route/{city}".format(city=data['taiwan'][city]),
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


@app.route('/v1/stop/<city>/<route>/', strict_slashes=False)
def get_stop(city, route):
    """取得該城市符合條件的所有路線站牌資料"""

    try:
        # 從 PTX 取得資料
        bus_stops = ptx.get("/v2/Bus/StopOfRoute/{city}/{route}".format(city=data['taiwan'][city], route=route),
                            params={'$select': 'RouteUID,RouteName,City,Direction,SubRouteUID,SubRouteName,Stops'})
    except KeyError:
        bus_stops = []
    # 取得該城市符合條件的所有路線到站估計資料
    try:
        # 從 PTX 取得資料
        bus_times = ptx.get("/v2/Bus/EstimatedTimeOfArrival/{city}/{route}".format(city=data['taiwan'][city], route=route),
                            params={'$select': 'StopUID,EstimateTime,StopStatus'})
    except KeyError:
        bus_times = []
    # 取得該城市符合條件的所有路線公車定位資料
    try:
        # 從 PTX 取得資料
        bus_reals = ptx.get("/v2/Bus/RealTimeNearStop/{city}/{route}".format(city=data['taiwan'][city], route=route),
                            params={'$select': 'StopUID,PlateNumb,BusStatus,A2EventType'})
    except KeyError:
        bus_reals = []

    # 處理資料
    result = []
    for bus_stop in bus_stops:
        # 在 SubRouteUID 後方加入 Direction
        try:
            bus_stop['SubRouteUID'] += str(bus_stop['Direction'])
        except KeyError:
            pass

        # 記錄停靠站
        stop_list = []
        for stop in bus_stop['Stops']:
            # 新增停靠站
            stop_list.append({})
            # 停靠站辨識碼
            stop_list[-1]['stopUID'] = stop['StopUID']
            # 停靠站名稱
            stop_list[-1]['stopName'] = stop['StopName']['Zh_tw']
            # 停靠站到站時間
            try:
                stop_list[-1]['estimateTime'] = bus_times[list(
                    map(lambda x: x['StopUID'], bus_times)).index(stop['StopUID'])]['EstimateTime']
            except KeyError:
                stop_list[-1]['estimateTime'] = -1
            except ValueError:
                stop_list[-1]['estimateTime'] = -1
            # 停靠站停靠狀態
            try:
                stop_list[-1]['stopStatus'] = bus_times[list(
                    map(lambda x: x['StopUID'], bus_times)).index(stop['StopUID'])]['StopStatus']
            except KeyError:
                stop_list[-1]['stopStatus'] = 0
            except ValueError:
                stop_list[-1]['stopStatus'] = 1
            # 車牌號碼
            stop_list[-1]['buses'] = []
            for bus_real in bus_reals:
                if bus_real['StopUID'] == stop['StopUID']:
                    # 新公車
                    stop_list[-1]['buses'].append({})
                    # 車牌號碼
                    stop_list[-1]['buses'][-1]['busNumber'] = bus_real['PlateNumb']
                    # 行車狀態
                    try:
                        stop_list[-1]['buses'][-1]['busStatus'] = bus_real['BusStatus']
                    except KeyError:
                        stop_list[-1]['buses'][-1]['busStatus'] = 0
                    # 進站離站
                    try:
                        stop_list[-1]['buses'][-1]['arriving'] = bus_real['A2EventType']
                    except KeyError:
                        stop_list[-1]['buses'][-1]['arriving'] = 0

        try:
            # 確認是否已經有該 UID 的資料
            exist = list(map(lambda x: x['routeUID'], result)).index(
                bus_stop['RouteUID'])
            # 確認是否已經有該 subRouteUID 的資料
            if not bus_stop['SubRouteUID'] in list(map(lambda x: x['subRouteUID'], result[exist]['subRoutes'])):
                # 沒有該 subRouteUID 的資料所以新增子路線
                result[exist]['subRoutes'].append({
                    # 子路線辨識碼
                    'subRouteUID': bus_stop['SubRouteUID'],
                    # 子路線名稱
                    'subRouteName': bus_stop['SubRouteName']['Zh_tw'].split('(')[0] + "（往" + stop_list[-1]['stopName'] + "）",
                    # 停靠站列表
                    'stops': stop_list,
                })
        except ValueError:
            # 沒有該 UID 的資料所以新增資料
            result.append({})
            # 路線辨識碼
            result[-1]['routeUID'] = bus_stop['RouteUID']
            # 路線名稱
            result[-1]['routeName'] = bus_stop['RouteName']['Zh_tw']
            # 城市
            try:
                result[-1]['city'] = bus_stop['City']
            except KeyError:
                result[-1]['city'] = city
            # 子路線
            result[-1]['subRoutes'] = [{
                # 子路線辨識碼
                'subRouteUID': bus_stop['SubRouteUID'],
                # 子路線名稱
                'subRouteName': bus_stop['SubRouteName']['Zh_tw'].split('(')[0] + "（往" + stop_list[-1]['stopName'] + "）",
                # 停靠站列表
                'stops': stop_list,
            }]

    # 回傳
    return jsonify({'routes': result})


def main():
    app.run(debug=True, threaded=True)


if __name__ == '__main__':
    main()
