import time
import hmac
import hashlib
import base64

import requests


class PTX:
    def __init__(self, app_id: str, app_key: str):
        self.__id = app_id
        self.__key = app_key

    def __signature(self):
        # 時間
        now = time.strftime('%a, %d %b %Y %H:%M:%S', time.gmtime()) + ' GMT'
        # 金鑰
        secret_key = bytes(self.__key, 'utf-8')
        # 訊息
        message = bytes('x-date: ' + now, 'utf-8')
        # 執行簽章
        digester = hmac.new(secret_key, message, hashlib.sha1).digest()
        signature = str(base64.b64encode(digester), 'utf-8')
        # 合成簽章字串
        authorization = 'hmac username="{id}", '.format(id=self.__id)
        authorization += 'algorithm="hmac-sha1", '
        authorization += 'headers="x-date", '
        authorization += 'signature="{signature}"'.format(signature=signature)
        # 回傳帶有 HMAC 簽章的 header
        return {
            'Accept': 'application/json',
            'Authorization': authorization,
            'x-date': now,
            'Accept-Encoding': 'gzip, deflate',
        }

    def get(self, res, params=None):
        """
        Make a GET request to get the resource which been needed.
        """

        # 判斷是否使用預設參數
        if params is None:
            # 預設參數
            params = {}
        # 要求取得 JSON 格式的資料
        params['$format'] = 'JSON'

        # 資源網址
        url = 'http://ptx.transportdata.tw/MOTC{res}'.format(res=res)

        # 回傳資源
        return requests.get(url, params, headers=self.__signature()).json()
