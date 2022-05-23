import json


class Loader:
    data = {}

    def importData(self, jsonpath):
        with open(jsonpath) as jsonfile:
            data = json.load(jsonfile)
            Loader.data = data
        return Loader.data
