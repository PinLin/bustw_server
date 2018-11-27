import sys

from .v1_stop import main as v1_stop_main
from .v1_real import main as v1_real_main
from .v1_time import main as v1_time_main


def main(city: str, route: str) -> dict:
    """取得該城市符合條件的所有路線站牌資料"""

    bus_stops = v1_stop_main(city, route)
    bus_times = v1_time_main(city, route)
    bus_reals = v1_real_main(city, route)

    result = {}
    for routeUID in bus_stops:
        # 先複製一份 bus_stop
        temp = bus_stops[routeUID].copy()

        for subRoute in temp['subRoutes']:
            # 在子路線名稱後加入目的地
            subRoute['subRouteName'] += "（往{}）".format(
                subRoute['stops'][-1]['stopName'])

            for stop in subRoute['stops']:
                for bus_time in bus_times:
                    # 跳過其他站
                    if stop['stopUID'] != bus_time['stopUID']:
                        continue
                    # 加入站牌估計時間
                    stop['estimateTime'] = bus_time['estimateTime']
                    # 加入站牌停靠狀態
                    stop['stopStatus'] = bus_time['stopStatus']
                    break

                stop['buses'] = []
                for bus_real in bus_reals:
                    # 跳過其他站
                    if stop['stopUID'] != bus_real['stopUID']:
                        continue
                    stop['buses'].append({
                        # 加入車牌號碼
                        'busNumber': bus_real['busNumber'],
                        # 加入行車狀態
                        'busStatus': bus_real['busStatus'],
                        # 加入進站離站
                        'arriving': bus_real['arriving'],
                    })

        result[temp['routeUID']] = temp

    # 回傳
    return result
