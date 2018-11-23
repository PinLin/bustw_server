import json


data = None


def read_from_file(path: str) -> dict:
    global data

    if data == None:
        f = open(path, 'r')
        data = json.load(f)
        f.close()

    return data
