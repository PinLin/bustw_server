import sys

from ..utils.taiwan import taiwan


def main() -> dict:
    """取得可用的城市列表"""
    result = []

    data = taiwan.cities

    for key in data:
        result.append({'key': key, 'name': data[key]['name']})

    return {'cities': result}


if __name__ == '__main__':
    main()
