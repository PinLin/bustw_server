import sys
from datetime import datetime
from ptx_api import PTX

from ..utils.taiwan import taiwan
from ..config import PTX_ID, PTX_KEY

cache = {}


def ptx_get(city: str) -> dict:
    """從 PTX 取得資料"""
    ptx = PTX(PTX_ID, PTX_KEY)

    return ptx.get("/v2/Bus/StopOfRoute/{city}".format(city=city),
                   params={'$select': 'RouteUID,RouteName,City,Direction,SubRouteUID,SubRouteName,Stops'})


def main(city: str, route: str) -> dict:
    """取得該城市符合條件的所有路線站牌資料"""
    global cache

    cities = {}
    data = taiwan.cities
    for key in data:
        cities[key] = data[key]['code']

    # 沒有這個縣市
    if not city in cities:
        bus_stops = []
    else:
        # 快取中不存在或快取過期
        if not city in cache or (datetime.now() - cache[city]['time']).total_seconds() > 10:
            # 更新快取
            cache[city] = {
                'time': datetime.now(),
                'data': ptx_get(cities[city]),
            }

        bus_stops = cache[city]['data']

    result = {}
    for bus_stop in bus_stops:
        temp = {
            # 路線辨識碼
            'routeUID': bus_stop['RouteUID'],
            # 路線名稱
            'routeName': bus_stop['RouteName']['Zh_tw'],
            # 城市
            'city': bus_stop.get('City') or city,
            # 子路線
            'subRoutes': [
                {
                    # 子路線辨識碼
                    'subRouteUID': bus_stop['SubRouteUID'] + str(bus_stop.get('Direction') or 0),
                    # 子路線名稱
                    'subRouteName': bus_stop['SubRouteName']['Zh_tw'].split('(')[0],
                    # 站牌列表
                    'stops': [{
                        # 站牌辨識碼
                        'stopUID': stop['StopUID'],
                        # 站牌名稱
                        'stopName': stop['StopName']['Zh_tw'],
                    } for stop in bus_stop['Stops']],
                }
            ]
        }

        # 如果有限制路線名稱就篩選
        if route != None and not route in temp['routeName']:
            continue

        # 如果有多條子路線就合併
        if temp['routeUID'] in result:
            result[temp['routeUID']]['subRoutes'].append(temp['subRoutes'][0])
        else:
            result[temp['routeUID']] = temp

    # 回傳
    return result
