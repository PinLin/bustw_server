import sys

from ..utils import city


def main() -> dict:
    result = []

    data = city.read_from_file(sys.path[0] + '/bustw_server/taiwan.json')

    for key in data:
        result.append({'key': key, 'name': data[key]['name']})

    return {'cities': result}


if __name__ == '__main__':
    main()
