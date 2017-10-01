""" json_encoder """
import json
import datetime

import arrow

from bson.objectid import ObjectId

class MyJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return arrow.get(obj).isoformat()
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)