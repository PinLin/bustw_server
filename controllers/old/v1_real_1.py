from utils.taiwan import taiwan
from utils.cache import real_cache


def main(city: str, route: str) -> list:
    """取得該城市符合條件的所有路線定位資料"""
    cities = {}
    data = taiwan.cities
    for key in data:
        cities[key] = data[key]['code']

    bus_reals = real_cache.get(cities[city], route or '')

    result = []
    for bus_real in bus_reals:
        temp = {
            # 路線辨識碼
            'routeUID': bus_real['RouteUID'],
            # 路線名稱
            'routeName': bus_real['RouteName']['Zh_tw'],
            # 車牌號碼
            'busNumber': bus_real['PlateNumb'],
            # 站牌辨識碼
            'stopUID': bus_real['StopUID'],
            # 站牌名稱
            'stopName': bus_real['StopName']['Zh_tw'],
            # 行車狀態
            'busStatus': bus_real.get('BusStatus') or 0,
            # 進站離站
            'arriving': bus_real.get('A2EventType') or 0,
        }

        result.append(temp)

    # 回傳
    return result
