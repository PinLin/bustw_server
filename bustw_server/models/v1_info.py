import sys
from ptx_api import PTX

from ..utils import taiwan
from ..config import PTX_ID, PTX_KEY


def main(city: str) -> dict:
    cities = {}

    data = taiwan.read_from_file(sys.path[0] + '/bustw_server/taiwan.json')

    for key in data:
        cities[key] = data[key]['code']

    # 初始化 PTX
    ptx = PTX(PTX_ID, PTX_KEY)

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
    return {'routes': result}


if __name__ == '__main__':
    main("Taipei")
