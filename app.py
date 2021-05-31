from flask import jsonify, request
from flask import Flask
from services import info, stop, real, time, aio

# 初始化 Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def say_hi():
    """顯示歡迎訊息"""
    return {
        'message': "Welcome to bustw_server!",
    }


@app.route('/info/<city>', defaults={'route': None}, strict_slashes=False)
@app.route('/info/<city>/<route>', strict_slashes=False)
def get_info(city, route):
    """取得該城市符合條件的所有路線基本資料"""
    return jsonify(info.main(city, route))


@app.route('/stop/<city>/<route>', strict_slashes=False)
def get_stop(city, route):
    """取得該城市符合條件的所有路線站牌資料"""
    return jsonify(stop.main(city, route))


@app.route('/real/<city>/<route>', strict_slashes=False)
def get_real(city, route):
    """取得該城市符合條件的所有路線定位資料"""
    return jsonify(real.main(city, route))


@app.route('/time/<city>/<route>', strict_slashes=False)
def get_time(city, route):
    """取得該城市符合條件的所有路線時間資料"""
    return jsonify(time.main(city, route))


@app.route('/aio/<city>/<route>', strict_slashes=False)
def get_aio(city, route):
    """取得該城市符合條件的所有路線站牌資料"""
    return jsonify(aio.main(city, route))


def main():
    app.run(debug=True, threaded=True)


if __name__ == '__main__':
    main()
