#!/usr/bin/env python3

from flask import Blueprint, jsonify


# 初始化 city 藍圖
v1_api = Blueprint('v1', __name__)


@v1_api.route('/v1/city/', strict_slashes=False)
def v1_city():
    """取得可用的城市列表"""
    pass


@v1_api.route('/v1/info/<city>/', strict_slashes=False)
def v1_info(city):
    """取得該城市符合條件的所有路線"""
    pass


@v1_api.route('/v1/stop/<city>/<route>/', strict_slashes=False)
def v1_stop(city, route):
    """取得該城市符合條件的所有路線站牌資料"""
    pass
