from bustw_server import app


def main():
    app.run(debug=True, threaded=True)


if __name__ == '__main__':
    main()
