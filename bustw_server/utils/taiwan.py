import sys
import json


class Taiwan:
    def __init__(self):
        self.__cities = None

    def load_cities(self, path: str):
        f = open(path, 'r')
        self.__cities = json.load(f)
        f.close()

    @property
    def cities(self) -> dict:
        return self.__cities


taiwan = Taiwan()
taiwan.load_cities(sys.path[0] + '/bustw_server/taiwan.json')
