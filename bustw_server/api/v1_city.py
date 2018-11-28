import sys

from ..utils.taiwan import taiwan


def main(city: str) -> list:
    """取得可用的城市列表資料"""
    result = []

    data = taiwan.cities

    for key in data:
        result.append({'key': key, 'name': data[key]['name']})

    return result
