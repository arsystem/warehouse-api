""" penerimaan_barang.py """
import falcon

from lib.model.penerimaan_barang import PenerimaanBarang
from lib.helper.penerimaan_barang import PenerimaanBarangHelper

class ListPenerimaanBarangListener:
    """ ListPenerimaanBarangListener """
    def on_post(self, req, res):
        """ handle POST requests """
        penerimaan_barang = PenerimaanBarangHelper.parse_from_body_request(req)
        inserted_id = PenerimaanBarangHelper.save(penerimaan_barang)
        req.context["result"] = {
            "data": {"inserted_id": str(inserted_id)},
            "status": {"code": 200, "message": "success"}
        }

    def on_get(self, req, res):
        """ handle GET requests """
        start_tanggal_terima = req.get_param("start_tanggal_terima") or None
        end_tanggal_terima = req.get_param("end_tanggal_terima") or None
        start_tanggal_entri = req.get_param("start_tanggal_entri") or None
        end_tanggal_entri = req.get_param("end_tanggal_entri") or None

        penerimaan_barang = PenerimaanBarangHelper.parse_from_query_string_request(req)
        list_penerimaan_barang = PenerimaanBarangHelper.find(
            penerimaan_barang, start_tanggal_entri, end_tanggal_entri,
            start_tanggal_terima, end_tanggal_terima
        )
        req.context["result"] = {
            "data": [penerimaan_barang.to_dict() for penerimaan_barang in list_penerimaan_barang],
            "status": {"code": 200, "message": "success"}
        }
        res.status = falcon.HTTP_200

class PenerimaanBarangListener:
    """ PenerimaanBarangListener """
    def on_get(self, req, res, _id):
        """ handle GET requests """
        penerimaan_barang = PenerimaanBarang()
        penerimaan_barang.id = _id
        penerimaan_barang = PenerimaanBarangHelper.get_detail(penerimaan_barang)
        req.context["result"] = {"data": penerimaan_barang.to_dict(), "status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200