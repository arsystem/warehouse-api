""" login.py """
import falcon

from lib.helper.user import UserHelper
from lib.model.user import User
from lib.exception import NoBodyException

class LoginListener:
    """ LoginListener """
    def on_post(self, req, res):
        """ handle POST requests """
        if "body" not in req.context:
            raise NoBodyException()
        body = req.context["body"]
        user = User()
        user.id = body["id"]
        user.password = body["password"]
        success = UserHelper.login(user)

        req.context["result"] = {"status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200
        if not success:
            req.context["result"] = {"status": {"code": 404, "message": "not auhorized"}}
            res.status = falcon.HTTP_404
