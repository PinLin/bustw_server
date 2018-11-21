import sys
import json

from flask import Flask, jsonify

from .route import v1_api

# 初始化 Flask
app = Flask(__name__)


# 註冊藍圖
app.register_blueprint(v1_api)


def main():
    app.run(debug=True, threaded=True)


if __name__ == '__main__':
    main()
