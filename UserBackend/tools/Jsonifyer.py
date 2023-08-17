import inspect
import json

class Jsonifyer:
    types = [int, str, float, type(None)]
    def getJson(self) -> str:
        result = json.dumps(self.getParamsList())
        return result

    def getParamsList(self) -> object:
        result = {}
        for i in inspect.getmembers(self):
                if not i[0].startswith('_'):
                    if not inspect.ismethod(i[1]):
                        if type(i[1]) in self.types:
                            result[i[0]] = i[1]
        return result