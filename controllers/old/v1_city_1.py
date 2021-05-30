from utils.taiwan import taiwan


def main() -> list:
    """取得可用的城市列表"""
    result = []

    data = taiwan.cities

    for key in data:
        temp = {
            'key': key, 'name': data[key]['name']
        }

        result.append(temp)

    return result
