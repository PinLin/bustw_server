from flask import jsonify, request
from flask import Flask
from controllers.old import v1_stop_2
from controllers.old import v1_city_1, v1_info_1, v1_stop_1, v1_real_1, v1_time_1
from controllers import v1_root, v1_city, v1_info, v1_stop, v1_real, v1_time

# 初始化 Flask
app = Flask(__name__)


@app.route('/v1', strict_slashes=False)
def root():
    """顯示歡迎訊息"""
    return jsonify(v1_root.main())


@app.route('/v1/city/', strict_slashes=False)
def city():
    """取得可用的城市列表資料"""
    version = request.args.get('ver')
    if not version or int(version) <= 2:
        # v1_city v1
        return jsonify(v1_city_1.main())

    else:
        # v1_city v3
        return jsonify(v1_city.main())


@app.route('/v1/info/<city>/', defaults={'route': None}, strict_slashes=False)
@app.route('/v1/info/<city>/<route>', strict_slashes=False)
def info(city, route):
    """取得該城市符合條件的所有路線基本資料"""
    version = request.args.get('ver')
    if not version or int(version) <= 2:
        # v1_info v1
        return jsonify(v1_info_1.main(city, route))

    else:
        # v1_info v3
        return jsonify(v1_info.main(city, route))


@app.route('/v1/stop/<city>/<route>/', strict_slashes=False)
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


@app.route('/v1/real/<city>/<route>/', strict_slashes=False)
def real(city, route):
    """取得該城市符合條件的所有路線定位資料"""
    version = request.args.get('ver')
    if not version or int(version) <= 2:
        # v1_real v1
        return jsonify(v1_real_1.main(city, route))

    else:
        # v1_real v3
        return jsonify(v1_real.main(city, route))


@app.route('/v1/time/<city>/<route>/', strict_slashes=False)
def time(city, route):
    """取得該城市符合條件的所有路線時間資料"""
    version = request.args.get('ver')
    if not version or int(version) <= 2:
        # v1_time v1
        return jsonify(v1_time_1.main(city, route))

    else:
        # v1_time v3
        return jsonify(v1_time.main(city, route))


def main():
    app.run(debug=True, threaded=True)


if __name__ == '__main__':
    main()
