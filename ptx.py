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
    def city_routes(self, city:str):
        # API 網址
        url = "http://ptx.transportdata.tw/MOTC/v2/Bus/Route/{city}?$format=json".format(city=city)
        # 取得資料
        response = requests.get(url, headers=self.headers, timeout=self.timeout)
        # 如果成功就回傳
        if response.status_code == 200:
            return json.loads(response.text)
        else:
            return {}