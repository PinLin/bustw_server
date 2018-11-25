import sys
from ptx_api import PTX

from ..utils.taiwan import taiwan
from ..config import PTX_ID, PTX_KEY


def main(city: str) -> dict:
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
        temp = {}

        # 路線辨識碼
        temp['routeUID'] = bus_route['RouteUID']
        # 路線名稱
        temp['routeName'] = bus_route['RouteName']['Zh_tw']
        # 城市名稱
        try:
            temp['city'] = bus_route['City']
        except KeyError:
            temp['city'] = city
        # 起站名稱
        try:
            temp['departureStopName'] = bus_route['DepartureStopNameZh']
        except KeyError:
            temp['departureStopName'] = ''
        # 終站名稱
        try:
            temp['destinationStopName'] = bus_route['DestinationStopNameZh']
        except KeyError:
            temp['destinationStopName'] = ''

        result.append(temp)

    # 回傳
    return {'routes': result}


if __name__ == '__main__':
    main("Taipei")
