#!/usr/bin/env python3

import requests
import sys
import json
import time
import hmac
import hashlib
import base64

class PTX:
    def __init__(self, app:dict={}, timeout:int=5):
        # 設定 App ID
        try:
            self.app_id = app['id']
        except KeyError:
            self.app_id = ''
        # 設定 App Key
        try:
            self.app_key = app['key']
        except KeyError:
            self.app_key = ''
        # 設定 request 的 headers
        self.headers = {}
        # 設定 request 最高等待秒數
        self.timeout = timeout
    
    # 驗證 headers
    def verify_headers(self):
        if self.app_id != '' and self.app_key != '':
            # 現在時間
            now = time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime()) + ' GMT'
            # 簽名
            digester = hmac.new(bytes(self.app_key, 'utf-8'), bytes('x-date: ' + now, 'utf-8'), hashlib.sha1).digest()
            signature = str(base64.b64encode(digester), 'utf-8')
            
            # 產生有 HMAC 簽章的 headers
            self.headers = {
                'Accept': 'application/json',
                'Authorization': 'hmac username="' + self.app_id + '", algorithm="hmac-sha1", headers="x-date", signature="' + signature + '"',
                'x-date': now,
                'Accept-Encoding': 'gzip, deflate',
            }
        else:
            # 使用測試用的 headers
            self.headers = {
                'User-Agent': 'Mozilla',
                'Accept': 'application/json',
                'Accept-Encoding': 'gzip, deflate',
            }
            # 提示訊息
            print("PTX - [⚠️ Warning] You haven't enter App ID and App Key.", file=sys.stderr)

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
        
        # 提示訊息
        print("PTX - [ℹ️ Info] Getting bus_route...", file=sys.stderr)
        # 驗證 headers
        self.verify_headers()
        # 向 PTX 平台取得資料
        try:
            # 取得資料
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            # 提示訊息
            print("PTX - [❌ Error] bus_route Timeout", file=sys.stderr)

        # 判斷請求是否成功
        if response.status_code != 200:
            # 提示訊息
            print("PTX - [❌ Error] Failed to Get bus_route. Code:", response.status_code, file=sys.stderr)
            # 回傳
            return []
        else:
            # 回傳
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
        
        # 提示訊息
        print("PTX - [ℹ️ Info] Getting bus_stop...", file=sys.stderr)
        # 驗證 headers
        self.verify_headers()
        # 向 PTX 平台取得資料
        try:
            # 取得資料
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            # 提示訊息
            print("PTX - [❌ Error] bus_stop Timeout", file=sys.stderr)
        
        # 判斷請求是否成功
        if response.status_code != 200:
            # 提示訊息
            print("PTX - [❌ Error] Failed to Get bus_stop. Code:", response.status_code, file=sys.stderr)
            # 回傳
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
        
        # 提示訊息
        print("PTX - [ℹ️ Info] Getting bus_time...", file=sys.stderr)
        # 驗證 headers
        self.verify_headers()
        # 向 PTX 平台取得資料
        try:
            # 取得資料
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            # 提示訊息
            print("PTX - [❌ Error] bus_time Timeout", file=sys.stderr)
        
        # 判斷請求是否成功
        if response.status_code != 200:
            # 提示訊息
            print("PTX - [❌ Error] Failed to Get bus_time. Code:", response.status_code, file=sys.stderr)
            # 回傳
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
        
        # 提示訊息
        print("PTX - [ℹ️ Info] Getting bus_real...", file=sys.stderr)
        # 驗證 headers
        self.verify_headers()
        # 向 PTX 平台取得資料
        try:
            # 取得資料
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
        except requests.exceptions.Timeout:
            # 提示訊息
            print("PTX - [❌ Error] bus_real Timeout", file=sys.stderr)
        
        # 判斷請求是否成功
        if response.status_code != 200:
            # 提示訊息
            print("PTX - [❌ Error] Failed to Get bus_real. Code:", response.status_code, file=sys.stderr)
            # 回傳
            return []
        else:
            return json.loads(response.text)
