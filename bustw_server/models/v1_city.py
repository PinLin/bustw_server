import sys

from ..utils import taiwan


def main() -> dict:
    result = []

    data = taiwan.read_from_file(sys.path[0] + '/bustw_server/taiwan.json')

    for key in data:
        result.append({'key': key, 'name': data[key]['name']})

    return {'cities': result}


if __name__ == '__main__':
    main()
