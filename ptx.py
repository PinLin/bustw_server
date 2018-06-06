#!/usr/bin/env python3

import requests
import json

class PTX:
    def __init__(self, timeout:int=5, headers:dict={}):
        # 設定 request 最高等待秒數
        self.timeout = timeout
        # 設定 request 的 headers
        self.headers = headers or {
            'User-Agent': 'Mozilla',
            'Accept': 'application/json',
            'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        }

    # 取得特定縣市路線資訊
    def bus_routes(self, city:str, route:str=''):
        # 所有路線資訊
        if route == '':
            # API 網址
            url = "http://ptx.transportdata.tw/MOTC/v2/Bus/Route/{city}?$format=JSON"\
                .format(city=city)
        # 搜尋特定路線資訊
        else:
            # API 網址
            url = "http://ptx.transportdata.tw/MOTC/v2/Bus/Route/{city}/{route}?$format=JSON"\
                .format(city=city, route=route)
        # 取得資料
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        # 如果成功就回傳
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {}
