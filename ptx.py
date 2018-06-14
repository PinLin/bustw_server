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
    def bus_route(self, city:str, name:str=None):
        # 所有路線資訊
        if name == None:
            # API 網址
            url = "http://ptx.transportdata.tw/MOTC/v2/Bus/Route/{city}?$format=JSON"\
                .format(city=city)
        # 搜尋特定路線資訊
        else:
            # API 網址
            url = "http://ptx.transportdata.tw/MOTC/v2/Bus/Route/{city}/{name}?$format=JSON"\
                .format(city=city, name=name)
        # 取得資料
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        # 判斷請求是否成功
        if response.status_code != 200:
            return {}
        else:
            return json.loads(response.text)

    # 取得特定縣市站牌資訊
    def bus_stop(self, city:str, name:str=None):
        # 所有站牌資訊
        if name == None:
            # API 網址
            url = "http://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/{city}?$format=JSON"\
                .format(city=city)
        # 搜尋特定站牌資訊
        else:
            # API 網址
            url = "http://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/{city}/{name}?$format=JSON"\
                .format(city=city, name=name)
        # 取得資料
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        # 判斷請求是否成功
        if response.status_code != 200:
            return {}
        else:
            return json.loads(response.text)
