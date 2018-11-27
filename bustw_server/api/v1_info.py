import sys
from ptx_api import PTX

from ..utils.taiwan import taiwan
from ..config import PTX_ID, PTX_KEY


def main(city: str, route: str) -> dict:
    """取得該城市符合條件的所有路線基本資料"""
    cities = {}

    data = taiwan.cities
    for key in data:
        cities[key] = data[key]['code']

    ptx = PTX(PTX_ID, PTX_KEY)
    try:
        # 從 PTX 取得資料
        bus_routes = ptx.get("/v2/Bus/Route/{city}".format(city=cities[city]),
                             params={'$select': 'RouteUID,RouteName,City,DepartureStopNameZh,DestinationStopNameZh'})
    except KeyError:
        bus_routes = []

    result = []
    for bus_route in bus_routes:
        temp = {
            # 路線辨識碼
            'routeUID': bus_route['RouteUID'],
            # 路線名稱
            'routeName': bus_route['RouteName']['Zh_tw'],
            # 城市名稱
            'city': bus_route.get('City') or city,
            # 起站名稱
            'departureStopName': bus_route.get('DepartureStopNameZh') or '',
            # 終站名稱
            'destinationStopName': bus_route.get('DestinationStopNameZh') or '',
        }

        # 如果有限制路線名稱就篩選
        if route != None and not route in temp['routeName']:
            continue

        result.append(temp)

    # 回傳
    return {'routes': result}
