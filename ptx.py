#!/usr/bin/env python3

import requests
import json

class PTX:
    def __init__(self, timeout:int=5, appid:str='', appkey:str=''):
        # 設定 request 最高等待秒數
        self.timeout = timeout
        # 設定 App ID
        self.appid = appid
        # 設定 App Key
        self.appkey = appkey
        # 設定 request 的 headers
        self.headers = {}
    
    # 驗證 headers
    def verify_headers(self):
        if self.appid != '' and self.appkey != '':
            # 產生有 HMAC 簽章的 headers
            pass
        else:
            # 使用測試用的 headers
            self.headers = {
                'User-Agent': 'Mozilla',
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            }

    # 取得特定縣市路線基本資訊
    def bus_route(self, city:str, route_name:str=None, arg:dict={}):
        # 所有資訊
        if route_name == None:
            # API 網址
            url = "http://ptx.transportdata.tw/MOTC/v2/Bus/Route/{city}?$format=JSON"\
                .format(city=city)
        # 搜尋特定資訊
        else:
            # API 網址
            url = "http://ptx.transportdata.tw/MOTC/v2/Bus/Route/{city}/{route_name}?$format=JSON"\
                .format(city=city, route_name=route_name)
        
        # 加上引數
        for item in arg.items():
            url += '&{key}={value}'.format(key=item[0], value=item[1])
        
        # 驗證 headers
        self.verify_headers()
        # 取得資料
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        
        # 判斷請求是否成功
        if response.status_code != 200:
            return []
        else:
            return json.loads(response.text)

    # 取得特定縣市路線站牌資訊
    def bus_stop(self, city:str, route_name:str=None, arg:dict={}):
        # 所有資訊
        if route_name == None:
            # API 網址
            url = "http://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/{city}?$format=JSON"\
                .format(city=city)
        # 搜尋特定資訊
        else:
            # API 網址
            url = "http://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/{city}/{route_name}?$format=JSON"\
                .format(city=city, route_name=route_name)
        
        # 加上引數
        for item in arg.items():
            url += '&{key}={value}'.format(key=item[0], value=item[1])
        
        # 驗證 headers
        self.verify_headers()
        # 取得資料
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        
        # 判斷請求是否成功
        if response.status_code != 200:
            return []
        else:
            return json.loads(response.text)

    # 取得特定縣市路線到站資訊
    def bus_time(self, city:str, route_name:str=None, arg:dict={}):
        # 所有資訊
        if route_name == None:
            # API 網址
            url = "http://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/{city}?$format=JSON"\
                .format(city=city)
        # 搜尋特定資訊
        else:
            # API 網址
            url = "http://ptx.transportdata.tw/MOTC/v2/Bus/EstimatedTimeOfArrival/{city}/{route_name}?$format=JSON"\
                .format(city=city, route_name=route_name)
        
        # 加上引數
        for item in arg.items():
            url += '&{key}={value}'.format(key=item[0], value=item[1])
        
        # 驗證 headers
        self.verify_headers()
        # 取得資料
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        
        # 判斷請求是否成功
        if response.status_code != 200:
            return []
        else:
            return json.loads(response.text)

    # 取得特定縣市路線動態資訊
    def bus_real(self, city:str, route_name:str=None, arg:dict={}):
        # 所有資訊
        if route_name == None:
            # API 網址
            url = "http://ptx.transportdata.tw/MOTC/v2/Bus/RealTimeNearStop/{city}?$format=JSON"\
                .format(city=city)
        # 搜尋特定資訊
        else:
            # API 網址
            url = "http://ptx.transportdata.tw/MOTC/v2/Bus/RealTimeNearStop/{city}/{route_name}?$format=JSON"\
                .format(city=city, route_name=route_name)
        
        # 加上引數
        for item in arg.items():
            url += '&{key}={value}'.format(key=item[0], value=item[1])
        
        # 驗證 headers
        self.verify_headers()
        # 取得資料
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        
        # 判斷請求是否成功
        if response.status_code != 200:
            return []
        else:
            return json.loads(response.text)
