from flask import jsonify, request
from flask import Flask
from controllers import v1_root, v1_info, v1_stop, v1_real, v1_time, v1_stop_old

# 初始化 Flask
app = Flask(__name__)


@app.route('/v1', strict_slashes=False)
def root():
    """顯示歡迎訊息"""
    return jsonify(v1_root.main())


@app.route('/v1/info/<city>/', defaults={'route': None}, strict_slashes=False)
@app.route('/v1/info/<city>/<route>', strict_slashes=False)
def info(city, route):
    """取得該城市符合條件的所有路線基本資料"""
    return jsonify(v1_info.main(city, route))


@app.route('/v1/stop/<city>/<route>/', strict_slashes=False)
def stop(city, route):
    """取得該城市符合條件的所有路線站牌資料"""
    version = request.args.get('ver')
    if not version or int(version) <= 1:
        return jsonify(v1_stop_old.main(city, route))

    else:
        return jsonify(v1_stop.main(city, route))


@app.route('/v1/real/<city>/<route>/', strict_slashes=False)
def real(city, route):
    """取得該城市符合條件的所有路線定位資料"""
    return jsonify(v1_real.main(city, route))


@app.route('/v1/time/<city>/<route>/', strict_slashes=False)
def time(city, route):
    """取得該城市符合條件的所有路線時間資料"""
    return jsonify(v1_time.main(city, route))


def main():
    app.run(debug=True, threaded=True)


if __name__ == '__main__':
    main()
