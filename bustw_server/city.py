#!/usr/bin/env python3

import sys
import json

from flask import Blueprint, jsonify

# 載入縣市資料對照表
with open(sys.path[0] + '/bustw_server/taiwan.json', 'r') as f:
    data = json.load(f)

# 取得縣市中英文名稱
cities = []
for key in data:
    cities.append({'key': key, 'name': data[key]['name']})

# 初始化 city 藍圖
city_api = Blueprint('city', __name__)


@city_api.route('/v1/city/', strict_slashes=False)
def list_city():
    """取得可用的城市列表"""

    return jsonify({'cities': cities})
