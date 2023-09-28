import inspect
import json
from datetime import datetime
class Jsonifyer:
    types = [int, str, float, type(None), type(datetime.now())]
    def getJson(self) -> str:
        result = json.dumps(self.getParamsList())
        return result

    def getParamsList(self, exceptions = []) -> object:
        result = {}
        for i in inspect.getmembers(self):
                if not i[0].endswith('_'):
                    if not inspect.ismethod(i[1]):
                        if type(i[1]) in self.types:
                            if i[0] not in exceptions:
                                result[i[0]] = i[1]
        return result