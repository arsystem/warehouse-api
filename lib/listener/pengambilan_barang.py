""" pengambilan_barang.py """
import falcon

from lib.model.pengambilan_barang import PengambilanBarang
from lib.helper.pengambilan_barang import PengambilanBarangHelper

class ListPengambilanBarangListener:
    """ ListPengambilanBarangListener """
    def on_post(self, req, res):
        """ handel POST requests """
        pengambilan_barang = PengambilanBarangHelper.parse_from_body_request(req)
        inserted_id = PengambilanBarangHelper.save(pengambilan_barang)
        req.context["result"] = {"data": {"inserted_id": str(inserted_id)}, "status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

    def on_get(self, req, res):
        """ handle GET requests """
        start_tanggal_ambil = req.get("start_tanggal_ambil") or None
        end_tanggal_ambil = req.get("end_tanggal_ambil") or None
        start_tanggal_entri = req.get("start_tanggal_entri") or None
        end_tanggal_entri = req.get("end_tanggal_entri") or None
        pengambilan_barang = PengambilanBarangHelper.parse_from_query_string(req)
        list_pengambilan_barang = PengambilanBarangHelper.find(
            pengambilan_barang, start_tanggal_entri, end_tanggal_entri,
            start_tanggal_ambil, end_tanggal_ambil
        )
        req.context["result"] = {
            "data": [pengambilan_barang.to_dict() for pengambilan_barang in list_pengambilan_barang],
            "status": {"code": 200, "message": "success"}
        }
        res.status = falcon.HTTP_200

class PengambilanBarangListener:
    """ PengambilanBarangListener """
    def on_get(self, req, res, _id):
        """ handle GET requests """
        pengambilan_barang = PengambilanBarang()
        pengambilan_barang.id = _id
        pengambilan_barang = PengambilanBarangHelper.get_detail(pengambilan_barang)
        req.context["result"] = {"data": pengambilan_barang.to_dict(), "status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200