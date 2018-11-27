import sys
from ptx_api import PTX

from ..utils.taiwan import taiwan
from ..config import PTX_ID, PTX_KEY


def main(city: str, route: str) -> list:
    """取得該城市符合條件的所有路線定位資料"""
    cities = {}

    data = taiwan.cities
    for key in data:
        cities[key] = data[key]['code']

    ptx = PTX(PTX_ID, PTX_KEY)
    try:
        # 從 PTX 取得資料
        bus_reals = ptx.get("/v2/Bus/RealTimeNearStop/{city}".format(city=cities[city]),
                            params={'$select': 'PlateNumb,RouteUID,RouteName,StopUID,StopName,BusStatus,A2EventType'})
    except KeyError:
        bus_reals = []

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

        # 如果有限制路線名稱就篩選
        if route != None and not route in temp['routeName']:
            continue

        result.append(temp)

    # 回傳
    return result
