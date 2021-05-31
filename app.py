from flask import jsonify, request
from flask import Flask
from services import info, stop, real, time, all_in_one

# 初始化 Flask
app = Flask(__name__)


@app.route('/v1', strict_slashes=False)
def say_hi():
    """顯示歡迎訊息"""
    return {
        'message': "Welcome to bustw_server!",
    }


@app.route('/v1/info/<city>/', defaults={'route': None}, strict_slashes=False)
@app.route('/v1/info/<city>/<route>', strict_slashes=False)
def get_info(city, route):
    """取得該城市符合條件的所有路線基本資料"""
    return jsonify(info.main(city, route))


@app.route('/v1/stop/<city>/<route>/', strict_slashes=False)
def get_stop(city, route):
    """取得該城市符合條件的所有路線站牌資料"""
    version = request.args.get('ver')
    if not version or int(version) <= 1:
        return jsonify(all_in_one.main(city, route))

    else:
        return jsonify(stop.main(city, route))


@app.route('/v1/real/<city>/<route>/', strict_slashes=False)
def get_real(city, route):
    """取得該城市符合條件的所有路線定位資料"""
    return jsonify(real.main(city, route))


@app.route('/v1/time/<city>/<route>/', strict_slashes=False)
def get_time(city, route):
    """取得該城市符合條件的所有路線時間資料"""
    return jsonify(time.main(city, route))


def main():
    app.run(debug=True, threaded=True)


if __name__ == '__main__':
    main()
