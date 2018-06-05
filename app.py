#!/usr/bin/env python3

from flask import Flask, request, Response
from pprint import pprint
import sys
import json

from ptx import PTX

# 初始化
api = PTX()
app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    # 讀取城市對應表
    with open(sys.path[0] + '/city_map.json', 'r') as f:
        city_map = json.load(f)
    # 使用者要查看哪個城市
    try:
        city = city_map[request.args['city']]
    except:
        city = ''
    # 取得該城市所有路線
    routes = api.city_routes(city)
    # 取出路線名稱部分
    data = []
    for route in routes:
        data.append(route['RouteName']['Zh_tw'])
    # 回傳
    return Response(json.dumps(data, ensure_ascii=False), mimetype='application/json')

def main():
    app.run("0.0.0.0", 65432)

if __name__ == '__main__':
    main()
