from utils.taiwan import taiwan
from utils.ptx_cache import time_cache


def main(city: str, route: str) -> list:
    """取得該城市符合條件的所有路線定位資料"""
    cities = {}
    data = taiwan.cities
    for key in data:
        cities[key] = data[key]['code']

    bus_times = time_cache.get(cities[city], route or '')

    result = []
    for bus_time in bus_times:
        temp = {
            # 路線辨識碼
            'routeUID': bus_time['RouteUID'],
            # 路線名稱
            'routeName': bus_time['RouteName']['Zh_tw'],
            # 站牌辨識碼
            'stopUID': bus_time['StopUID'],
            # 站牌名稱
            'stopName': bus_time['StopName']['Zh_tw'],
            # 估計時間
            'estimateTime': bus_time.get('EstimateTime') or -1,
            # 停靠狀態
            'stopStatus': bus_time.get('StopStatus') or 0,
        }

        result.append(temp)

    # 回傳
    return {'stops': result}
