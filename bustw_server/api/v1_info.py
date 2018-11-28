import sys
from datetime import datetime
from ptx_api import PTX

from ..utils.taiwan import taiwan
from ..config import PTX_ID, PTX_KEY

cache = {}


def ptx_get(city: str) -> dict:
    """從 PTX 取得資料"""
    ptx = PTX(PTX_ID, PTX_KEY)

    return ptx.get("/v2/Bus/Route/{city}".format(city=city),
                   params={'$select': 'RouteUID,RouteName,DepartureStopNameZh,DestinationStopNameZh,City'})


def main(city: str, route: str) -> dict:
    """取得該城市符合條件的所有路線基本資料"""
    global cache

    cities = {}
    data = taiwan.cities
    for key in data:
        cities[key] = data[key]['code']

    # 沒有這個縣市
    if not city in cities:
        bus_routes = []
    else:
        # 快取中不存在或快取過期
        if not city in cache or (datetime.now() - cache[city]['time']).total_seconds() > 43200:
            # 更新快取
            cache[city] = {
                'time': datetime.now(),
                'data': ptx_get(cities[city]),
            }

        bus_routes = cache[city]['data']

    result = {}
    for bus_route in bus_routes:
        temp = {
            # 路線辨識碼
            'routeUID': bus_route['RouteUID'],
            # 路線名稱
            'routeName': bus_route['RouteName']['Zh_tw'],
            # 城市名稱
            'city': city,
            # 起站名稱
            'departureStopName': bus_route.get('DepartureStopNameZh') or '',
            # 終站名稱
            'destinationStopName': bus_route.get('DestinationStopNameZh') or '',
        }

        # 如果有限制路線名稱就篩選
        if route != None and not route in temp['routeName']:
            continue

        result[temp['routeUID']] = temp

    # 回傳
    return result
