#!/usr/bin/env python3

import sys
import json

from flask import Flask, jsonify

from .route import v1_api

# 初始化 Flask
app = Flask(__name__)


@app.route('/v1/', strict_slashes=False)
def welcome():
    return jsonify({'message': "Welcome to bustw_server!"})


# 註冊藍圖
app.register_blueprint(v1_api)


def main():
    app.run(debug=True, threaded=True)


if __name__ == '__main__':
    main()
