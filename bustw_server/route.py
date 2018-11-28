import sys
from flask import Blueprint, jsonify, request, send_from_directory

from .api import v1_root, v1_city, v1_info, v1_stop, v1_real, v1_time
from .api import v1_stop_1


# 初始化 city 藍圖
v1_api = Blueprint('v1', __name__)


@v1_api.route('/v1/', strict_slashes=False)
def root():
    """顯示歡迎訊息"""
    return jsonify({
        'message': v1_root.main()
    })


@v1_api.route('/v1/docs/', defaults={'filename': 'index.html'}, strict_slashes=False)
@v1_api.route('/v1/docs/<filename>', strict_slashes=False)
def docs(filename):
    """swagger 說明文件"""
    return send_from_directory(sys.path[0] + '/bustw_server/docs', filename)


@v1_api.route('/v1/city/', defaults={'city': None}, strict_slashes=False)
@v1_api.route('/v1/city/<city>', strict_slashes=False)
def city(city):
    """取得可用的城市列表資料"""
    return jsonify({
        'cities': v1_city.main(city)
    })


@v1_api.route('/v1/info/<city>/', defaults={'route': None}, strict_slashes=False)
@v1_api.route('/v1/info/<city>/<route>', strict_slashes=False)
def info(city, route):
    """取得該城市符合條件的所有路線基本資料"""
    return jsonify({
        'routes': list(v1_info.main(city, route).values())
    })


@v1_api.route('/v1/stop/<city>/', defaults={'route': None}, strict_slashes=False)
@v1_api.route('/v1/stop/<city>/<route>/', strict_slashes=False)
def stop(city, route):
    """取得該城市符合條件的所有路線站牌資料"""
    if request.args.get('ver'):
        # 新版 v1_stop
        return jsonify({
            'routes': list(v1_stop.main(city, route).values())
        })

    else:
        # 舊版 v1_stop
        return jsonify({
            'routes': list(v1_stop_1.main(city, route).values())
        })


@v1_api.route('/v1/real/<city>/', defaults={'route': None}, strict_slashes=False)
@v1_api.route('/v1/real/<city>/<route>/', strict_slashes=False)
def real(city, route):
    """取得該城市符合條件的所有路線定位資料"""
    return jsonify({
        'buses': v1_real.main(city, route)
    })


@v1_api.route('/v1/time/<city>/', defaults={'route': None}, strict_slashes=False)
@v1_api.route('/v1/time/<city>/<route>/', strict_slashes=False)
def time(city, route):
    """取得該城市符合條件的所有路線時間資料"""
    return jsonify({
        'times': v1_time.main(city, route)
    })
