import falcon

from lib.helper.user import UserHelper
from lib.model.user import User

""" user.py """
class ListUserListener:
    """ ListUserListener """
    def on_post(self, req, res):
        """ handle POST requests """
        user = UserHelper.parse_from_body_request(req)
        UserHelper.save(user)
        req.context["result"] = {"status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

    def on_get(self, req, res):
        """ handle GET requests """
        user = UserHelper.parse_from_query_string_request(req)
        list_user = UserHelper.find(user)
        req.context["result"] = {"data": [user.to_dict() for user in list_user], "status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

class UserListener:
    """ UserListener """
    def on_get(self, req, res, _id):
        """ handle GET requests """
        user = User()
        user.id = _id
        user = UserHelper.get_detail(user)
        req.context["result"] = {"data": user.to_dict(), "status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

    def on_delete(self, req, res, _id):
        """ handle DELETE requests """
        user = User()
        user.id = _id
        UserHelper.delete(user)
        req.context["result"] = {"status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

    def on_put(self, req, res, _id):
        """ handle PUT requests """
        user = UserHelper.parse_from_query_string_request(req)
        user.id = _id
        UserHelper.update(user)
        req.context["result"] = {"status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200