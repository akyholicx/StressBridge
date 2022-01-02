import json

class Serializable:
    def toJSON(self): # python obj -> JSON
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True,separators=(',', ':'))

def serialize(d): # python list/dict -> JSON
    return json.dumps(d,separators=(',', ':'))

def deserialize(jsonString): # JSON -> python dict
    return json.loads(jsonString)




