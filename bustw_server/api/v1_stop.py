import sys
from ptx_api import PTX

from ..utils.taiwan import taiwan
from ..config import PTX_ID, PTX_KEY

# TODO: 暫時使用
from .v1_real import main as v1_real_main


def main(city: str, route: str) -> dict:
    """取得該城市符合條件的所有路線站牌資料"""
    cities = {}

    data = taiwan.cities
    for key in data:
        cities[key] = data[key]['code']

    ptx = PTX(PTX_ID, PTX_KEY)
    try:
        # 從 PTX 取得資料
        bus_stops = ptx.get("/v2/Bus/StopOfRoute/{city}/{route}".format(city=cities[city], route=route),
                            params={'$select': 'RouteUID,RouteName,City,Direction,SubRouteUID,SubRouteName,Stops'})
    except KeyError:
        bus_stops = []

    try:
        # 從 PTX 取得該城市符合條件的所有路線到站估計資料
        bus_times = ptx.get("/v2/Bus/EstimatedTimeOfArrival/{city}/{route}".format(city=cities[city], route=route),
                            params={'$select': 'StopUID,EstimateTime,StopStatus'})
    except KeyError:
        bus_times = []

    # 取得該城市符合條件的所有路線公車定位資料
    bus_reals = v1_real_main(city, route)['buses']

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
                if bus_real['stopUID'] != stop['StopUID']:
                    continue

                # 新公車
                stop_list[-1]['buses'].append({
                    # 車牌號碼
                    'busNumber': bus_real['busNumber'],
                    # 行車狀態
                    'busStatus': bus_real['busStatus'],
                    # 進站離站
                    'arriving': bus_real['arriving'],
                })

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
    return {'routes': result}
