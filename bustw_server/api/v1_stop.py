from ..utils.taiwan import taiwan
from ..utils.ptx_cache import stop_cache


def main(city: str, route: str) -> dict:
    """取得該城市符合條件的所有路線站牌資料"""
    cities = {}
    data = taiwan.cities
    for key in data:
        cities[key] = data[key]['code']

    bus_stops = stop_cache.get(cities[city], route or '')

    result = {}
    for bus_stop in bus_stops:
        temp = {
            # 路線辨識碼
            'routeUID': bus_stop['RouteUID'],
            # 路線名稱
            'routeName': bus_stop['RouteName']['Zh_tw'],
            # 城市英文名稱
            'city': bus_stop.get('City') or city,
            # 子路線列表
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

        # 如果有多條子路線就合併
        if temp['routeUID'] in result:
            result[temp['routeUID']]['subRoutes'].append(temp['subRoutes'][0])
        else:
            result[temp['routeUID']] = temp

    # 回傳
    return result
