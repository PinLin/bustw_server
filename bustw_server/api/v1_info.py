from ..utils.taiwan import taiwan
from ..utils.ptx_cache import info_cache


def main(city: str, route: str) -> dict:
    """取得該城市符合條件的所有路線基本資料"""
    cities = {}
    data = taiwan.cities
    for key in data:
        cities[key] = data[key]['code']

    bus_routes = info_cache.get(cities[city], route or '')

    result = {}
    for bus_route in bus_routes:
        temp = {
            # 路線辨識碼
            'routeUID': bus_route['RouteUID'],
            # 路線名稱
            'routeName': bus_route['RouteName']['Zh_tw'],
            # 城市英文名稱
            'city': city,
            # 起站名稱
            'departureStopName': bus_route.get('DepartureStopNameZh') or '',
            # 終站名稱
            'destinationStopName': bus_route.get('DestinationStopNameZh') or '',
        }

        result[temp['routeUID']] = temp

    result = list(result.values())

    # 回傳
    return result
