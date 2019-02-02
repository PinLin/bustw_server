import threading
from datetime import datetime
from ptx_api import PTX

from ..config import PTX as CONFIG


class PtxUpdater(threading.Thread):
    def __init__(self, source: dict, cache: dict, city: str):
        self.__url = source['url']
        self.__ptx = source['ptx']
        self.__params = source['params']
        self.__cache = cache
        self.__city = city

        super().__init__()

    def run(self):
        self.__cache[self.__city] = {
            'data': self.__ptx.get(self.__url + '/{city}'.format(city=self.__city), params=self.__params),
            'time': datetime.now(),
        }


class PtxCache:
    def __init__(self, timeout: int, url: str, params: dict=None):
        self.__url = url
        self.__params = params or {}
        self.__timeout = timeout

        self.__ptx = PTX(CONFIG['ID'], CONFIG['KEY'])
        self.__cache = {}

    def __valid(self, time: datetime) -> bool:
        return (datetime.now() - time).total_seconds() < self.__timeout

    def get(self, city: str, route: str=''):
        """取得該城市路線資料"""

        # 快取不存在或過期
        if not city in self.__cache or not self.__valid(self.__cache[city]['time']):
            # 先取得結果
            result = self.__ptx.get(
                self.__url + '/{city}/{route}'.format(city=city, route=route), params=self.__params)

            # 更新快取
            if route != '':
                # 另開執行緒進行更新
                PtxUpdater({
                    'url': self.__url,
                    'ptx': self.__ptx,
                    'params': self.__params,
                }, self.__cache, city).start()
            else:
                # 直接將結果存入
                self.__cache[city] = {
                    'data': result,
                    'time': datetime.now(),
                }

        # 快取可用
        else:
            # 對於路線名稱的處理
            if route != None:
                # 篩選名稱
                result = []
                for temp in self.__cache[city]['data']:
                    # 篩選
                    if not route in temp['RouteName']['Zh_tw']:
                        continue

                    result.append(temp)

            else:
                # 不做篩選
                result = self.__cache[city]['data']

        # 回傳結果
        return result


info_cache = PtxCache(43200, '/v2/Bus/Route',
                      {'$select': 'RouteUID,RouteName,DepartureStopNameZh,DestinationStopNameZh,City'})

real_cache = PtxCache(10, '/v2/Bus/RealTimeNearStop',
                      {'$select': 'PlateNumb,RouteUID,RouteName,StopUID,StopName,BusStatus,A2EventType'})

time_cache = PtxCache(10, '/v2/Bus/EstimatedTimeOfArrival',
                      {'$select': 'RouteUID,RouteName,StopUID,StopName,EstimateTime,StopStatus'})

stop_cache = PtxCache(43200, '/v2/Bus/StopOfRoute',
                      {'$select': 'RouteUID,RouteName,City,Direction,SubRouteUID,SubRouteName,Stops'})
