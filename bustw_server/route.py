import sys
from flask import Blueprint, jsonify, request, send_from_directory

from .api import v1_root, v1_city, v1_info, v1_stop, v1_real, v1_time
from .api.old import v1_city_1, v1_info_1, v1_stop_1, v1_real_1, v1_time_1
from .api.old import v1_stop_2


v1_api = Blueprint('v1', __name__)


@v1_api.route('/', strict_slashes=False)
def root():
    """顯示歡迎訊息"""
    return jsonify(v1_root.main())


@v1_api.route('/docs/', defaults={'filename': 'index.html'}, strict_slashes=False)
@v1_api.route('/docs/<filename>', strict_slashes=False)
def docs(filename):
    """swagger 說明文件"""
    return send_from_directory(sys.path[0] + '/bustw_server/docs', filename)


@v1_api.route('/city/', strict_slashes=False)
def city():
    """取得可用的城市列表資料"""
    version = request.args.get('ver')
    if not version or int(version) <= 2:
        # v1_city v1
        return jsonify(v1_city_1.main())

    else:
        # v1_city v3
        return jsonify(v1_city.main())


@v1_api.route('/info/<city>/', defaults={'route': None}, strict_slashes=False)
@v1_api.route('/info/<city>/<route>', strict_slashes=False)
def info(city, route):
    """取得該城市符合條件的所有路線基本資料"""
    version = request.args.get('ver')
    if not version or int(version) <= 2:
        # v1_info v1
        return jsonify(v1_info_1.main(city, route))

    else:
        # v1_info v3
        return jsonify(v1_info.main(city, route))


@v1_api.route('/stop/<city>/<route>/', strict_slashes=False)
def stop(city, route):
    """取得該城市符合條件的所有路線站牌資料"""
    version = request.args.get('ver')
    if not version or int(version) <= 1:
        # v1_stop v1
        return jsonify(v1_stop_1.main(city, route))

    elif int(version) <= 2:
        # v1_stop v2
        return jsonify(v1_stop_2.main(city, route))

    else:
        # v1_stop v3
        return jsonify(v1_stop.main(city, route))


@v1_api.route('/real/<city>/<route>/', strict_slashes=False)
def real(city, route):
    """取得該城市符合條件的所有路線定位資料"""
    version = request.args.get('ver')
    if not version or int(version) <= 2:
        # v1_real v1
        return jsonify(v1_real_1.main(city, route))

    else:
        # v1_real v3
        return jsonify(v1_real.main(city, route))


@v1_api.route('/time/<city>/<route>/', strict_slashes=False)
def time(city, route):
    """取得該城市符合條件的所有路線時間資料"""
    version = request.args.get('ver')
    if not version or int(version) <= 2:
        # v1_time v1
        return jsonify(v1_time_1.main(city, route))

    else:
        # v1_time v3
        return jsonify(v1_time.main(city, route))
