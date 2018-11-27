import sys
from ptx_api import PTX

from ..utils.taiwan import taiwan
from ..config import PTX_ID, PTX_KEY


def main(city: str, route: str) -> dict:
    """取得該城市符合條件的所有路線定位資料"""
    cities = {}

    data = taiwan.cities
    for key in data:
        cities[key] = data[key]['code']

    ptx = PTX(PTX_ID, PTX_KEY)
    try:
        # 從 PTX 取得資料
        bus_times = ptx.get("/v2/Bus/EstimatedTimeOfArrival/{city}".format(city=cities[city]),
                            params={'$select': 'RouteUID,RouteName,StopUID,StopName,EstimateTime,StopStatus'})
    except KeyError:
        bus_times = []

    result = {}
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
            'stopStatus': bus_time.get('StopStatus') or -1,
        }

        # 如果有限制路線名稱就篩選
        if route != None and not route in temp['routeName']:
            continue

        result[temp['routeUID']] = temp

    # 回傳
    return result
