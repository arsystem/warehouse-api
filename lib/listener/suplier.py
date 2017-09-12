""" suplier.py """
import falcon

from lib.model.suplier import Suplier
from lib.helper.suplier import SuplierHelper

class ListSuplierListener:
    """ ListSuplierListener """
    def on_post(self, req, res):
        """ handle POST requests """
        suplier = SuplierHelper.parse_from_body_request(req)
        inserted_id = SuplierHelper.save(suplier)
        req.context["result"] = {"status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

    def on_get(self, req, res):
        """ handle GET requests """
        suplier = SuplierHelper.parse_from_query_string_request(req)
        list_suplier = SuplierHelper.find(suplier)
        data = [suplier.to_dict() for suplier in list_suplier]
        req.context["result"] = {"data": data, "status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

class SuplierListener:
    """ SuplierListener """
    def on_get(self, req, res, _id):
        """ handle GET requests """
        suplier = Suplier()
        suplier.id = _id
        suplier = SuplierHelper.get_detail(suplier)

        if suplier is not None:
            req.context["result"] = {"data": suplier.to_dict(), "status": {"code": 200, "message": "success"}}
        else:
            req.context["result"] = {"data": {}, "status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

    def on_delete(self, req, res, _id):
        """ handle DELETE requests """
        suplier = Suplier()
        suplier.id = _id
        SuplierHelper.delete(suplier)
        req.context["result"] = {"status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

    def on_put(self, req, res, _id):
        """ handle PUT requests """
        suplier = SuplierHelper.parse_from_body_request(req)
        suplier.id = _id
        SuplierHelper.update(suplier)
        req.context["result"] = {"status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200