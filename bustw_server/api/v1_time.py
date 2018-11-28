import sys
from datetime import datetime
from ptx_api import PTX

from ..utils.taiwan import taiwan
from ..config import PTX_ID, PTX_KEY

cache = {}


def ptx_get(city: str) -> dict:
    """從 PTX 取得資料"""
    ptx = PTX(PTX_ID, PTX_KEY)

    return ptx.get("/v2/Bus/EstimatedTimeOfArrival/{city}".format(city=city),
                   params={'$select': 'RouteUID,RouteName,StopUID,StopName,EstimateTime,StopStatus'})


def main(city: str, route: str) -> list:
    """取得該城市符合條件的所有路線定位資料"""
    global cache

    cities = {}
    data = taiwan.cities
    for key in data:
        cities[key] = data[key]['code']

    # 沒有這個縣市
    if not city in cities:
        bus_times = []
    else:
        # 快取中不存在或快取過期
        if not city in cache or (datetime.now() - cache[city]['time']).total_seconds() > 10:
            # 更新快取
            cache[city] = {
                'time': datetime.now(),
                'data': ptx_get(cities[city]),
            }

        bus_times = cache[city]['data']

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

        # 如果有限制路線名稱就篩選
        if route != None and not route in temp['routeName']:
            continue

        result.append(temp)

    # 回傳
    return result
