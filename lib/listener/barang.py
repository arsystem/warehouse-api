""" barang.py """
import falcon

from lib.model.barang import Barang
from lib.helper.barang import BarangHelper

class ListBarangListener:
    """ BarangListListener """
    def on_post(self, req, res):
        """ handle POST requests """
        barang = BarangHelper.parse_from_body_request(req)
        insert_id = BarangHelper.save(barang)
        req.context["result"] = {"status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

    def on_get(self, req, res):
        """ handle GET requests """
        barang = BarangHelper.parse_from_query_string_request(req)
        list_barang = BarangHelper.find(barang)
        data = [barang.to_dict() for barang in list_barang]

        req.context["result"] = {
            "data": data,
            "status": {"code": 200, "message": "success"}
        }
        res.status = falcon.HTTP_200

class BarangListener:
    """ BarangListener """
    def on_get(self, req, res, barcode):
        """ handle GET requests """
        barang = Barang()
        barang.barcode = barcode
        barang = BarangHelper.get_detail(barang)
        req.context["result"] = {
            "data": barang.to_dict() if isinstance(barang, Barang) else {}, 
            "status": {"code": 200, "message": "success"}
        }
        res.status = falcon.HTTP_200

    def on_delete(self, req, res, barcode):
        """ handle DELETE requets """
        barang = Barang()
        barang.barcode = barcode
        BarangHelper.delete(barang)
        req.context["result"] = {"status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

    def on_put(self, req, res, barcode):
        """ handle PUT requests """
        barang = BarangHelper.parse_from_body_request(req)
        barang.barcode = barcode
        BarangHelper.update(barang)
        req.context["result"] = {"status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200