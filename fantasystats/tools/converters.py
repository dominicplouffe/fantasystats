from werkzeug.routing import BaseConverter, ValidationError
from bson.objectid import ObjectId
from bson.errors import InvalidId
import json


class ObjectIDConverter(BaseConverter):

    def to_python(self, value):
        try:
            return ObjectId(str(value))
        except (InvalidId, ValueError, TypeError):
            raise ValidationError()

    def to_url(self, value):
        return str(value)


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'strftime'):
            if obj.hour > 0 or obj.minute > 0:
                return obj.strftime('%Y-%m-%d %H:%M')
            else:
                return obj.strftime('%Y-%m-%d')
        if isinstance(obj, ObjectId):
            return str(obj)
        raise TypeError(
            "Unserializable object {} of type {}".format(obj, type(obj))
        )
