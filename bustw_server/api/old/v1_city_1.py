import sys

from ...utils.taiwan import taiwan


def main(city: str) -> list:
    """取得可用的城市列表"""
    result = []

    data = taiwan.cities

    for key in data:
        temp = {
            'key': key, 'name': data[key]['name']
        }

        # 如果有限制城市名稱就篩選
        if city != None and not city in temp['key']:
            continue

        result.append(temp)

    return result
