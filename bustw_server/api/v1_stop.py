import sys
from ptx_api import PTX

from ..utils.taiwan import taiwan
from ..config import PTX_ID, PTX_KEY

# TODO: 暫時使用
from .v1_real import main as v1_real_main
from .v1_time import main as v1_time_main


def get_stop(array, uid):
    try:
        stops = list(map(lambda x: x['stopUID'], array))
        index = stops.index(uid)
        return array[index]

    except ValueError:
        return {
            'estimateTime': 0,
            'stopStatus': 1,
        }


def main(city: str, route: str) -> dict:
    """取得該城市符合條件的所有路線站牌資料"""
    cities = {}

    data = taiwan.cities
    for key in data:
        cities[key] = data[key]['code']

    ptx = PTX(PTX_ID, PTX_KEY)
    try:
        # 從 PTX 取得資料
        bus_stops = ptx.get("/v2/Bus/StopOfRoute/{city}/{route}".format(city=cities[city], route=route),
                            params={'$select': 'RouteUID,RouteName,City,Direction,SubRouteUID,SubRouteName,Stops'})
    except KeyError:
        bus_stops = []

    # 取得該城市符合條件的所有路線時間資料
    bus_times = v1_time_main(city, route)['times']

    # 取得該城市符合條件的所有路線公車定位資料
    bus_reals = v1_real_main(city, route)['buses']

    result = []
    for bus_stop in bus_stops:
        # 在 SubRouteUID 後方加入 Direction
        bus_stop['SubRouteUID'] += str(bus_stop.get('Direction') or '')

        # 記錄停靠站
        stop_list = []
        for stop in bus_stop['Stops']:

            # 估計時間
            estimateTime = get_stop(bus_times, stop['StopUID']).get('estimateTime')
            # 停靠狀態
            stopStatus = get_stop(bus_times, stop['StopUID']).get('stopStatus')

            # 新增站牌
            stop_list.append({
                # 站牌辨識碼
                'stopUID': stop['StopUID'],
                # 站牌名稱
                'stopName': stop['StopName']['Zh_tw'],
                # 估計時間
                'estimateTime': estimateTime if estimateTime != None else -1,
                # 停靠狀態
                'stopStatus': stopStatus or 0,
            })

            # 車牌號碼
            stop_list[-1]['buses'] = []
            for bus_real in bus_reals:
                if bus_real['stopUID'] != stop['StopUID']:
                    continue

                # 新公車
                stop_list[-1]['buses'].append({
                    # 車牌號碼
                    'busNumber': bus_real['busNumber'],
                    # 行車狀態
                    'busStatus': bus_real['busStatus'],
                    # 進站離站
                    'arriving': bus_real['arriving'],
                })

        try:
            # 確認是否已經有該 UID 的資料
            exist = list(map(lambda x: x['routeUID'], result)).index(
                bus_stop['RouteUID'])
            # 確認是否已經有該 subRouteUID 的資料
            if not bus_stop['SubRouteUID'] in list(map(lambda x: x['subRouteUID'], result[exist]['subRoutes'])):
                # 沒有該 subRouteUID 的資料所以新增子路線
                result[exist]['subRoutes'].append({
                    # 子路線辨識碼
                    'subRouteUID': bus_stop['SubRouteUID'],
                    # 子路線名稱
                    'subRouteName': bus_stop['SubRouteName']['Zh_tw'].split('(')[0] + "（往" + stop_list[-1]['stopName'] + "）",
                    # 停靠站列表
                    'stops': stop_list,
                })
        except ValueError:
            # 沒有該 UID 的資料所以新增資料
            temp = {
                # 路線辨識碼
                'routeUID': bus_stop['RouteUID'],
                # 路線名稱
                'routeName': bus_stop['RouteName']['Zh_tw'],
                # 城市
                'city': bus_stop.get('City') or city,
                # 子路線
                'subRoutes': [
                    {
                        # 子路線辨識碼
                        'subRouteUID': bus_stop['SubRouteUID'],
                        # 子路線名稱
                        'subRouteName': bus_stop['SubRouteName']['Zh_tw'].split('(')[0] + "（往" + stop_list[-1]['stopName'] + "）",
                        # 停靠站列表
                        'stops': stop_list,
                    }
                ]
            }

            result.append(temp)

    # 回傳
    return {'routes': result}
