from falcon import HTTPError
import json
import falcon

class NoBodyException(HTTPError):
    def __init__(self):
        super(NoBodyException, self).__init__("", title=None, description=None, headers=None, href=None, href_text=None, code=None)
        self.code = 404
        self.message = "You need to provide JSON inside HTTP Body"
    
    def to_dict(self, obj_type):
        return {"status": {
            "code": self.code,
            "message": self.message
        }}

class FieldNotFoundException(HTTPError):
    def __init__(self, field=None):
        super(FieldNotFoundException, self).__init__("", title=None, description=None, headers=None, href=None, href_text=None, code=None)
        self.code = 404

        self.field = ""
        if field is not None:
            self.field = field

    def to_dict(self, obj_type):
        self.message = "Cannot find field: %s" % self.field
        return {"status": {
            "code": self.code,
            "message": self.message
        }}

class NotEnoughDataException(HTTPError):
    def __init__(self, field=None):
        super(NotEnoughDataException, self).__init__("", title=None, description=None, headers=None, href=None, href_text=None, code=None)
        self.code = 404
        self.message = "You need more data to be analyzed."

    def to_dict(self, obj_type):
        return {"status": {
            "code": self.code,
            "message": self.message
        }}

class TrackNotFoundException(HTTPError):
    def __init__(self, field=None):
        super(TrackNotFoundException, self).__init__("", title=None, description=None, headers=None, href=None, href_text=None, code=None)
        self.code = 404
        self.status = falcon.HTTP_404
        self.message = "Track not found."

    def to_dict(self, obj_type):
        return {"status": {
            "code": self.code,
            "message": self.message
        }}

class ModelNotTrainedException(HTTPError):
    def __init__(self, field=None):
        super(ModelNotTrainedException, self).__init__("", title=None, description=None, headers=None, href=None, href_text=None, code=None)
        self.code = 404
        self.message = "Model not trained."

    def to_dict(self, obj_type):
        return {"status": {
            "code": self.code,
            "message": self.message
        }}