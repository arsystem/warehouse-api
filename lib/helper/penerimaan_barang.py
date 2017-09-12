""" penerimaan_barang.py """
import pymongo
import arrow

from bson.objectid import ObjectId

from lib.model.penerimaan_barang import PenerimaanBarang
from lib.model.user import User
from lib.model.suplier import Suplier
from lib.helper.barang import BarangHelper
from lib.helper.user import UserHelper
from lib.helper.suplier import SuplierHelper
from lib.exception import NoBodyException
from lib.config import Config

class PenerimaanBarangHelper:
    """ PenerimaanBarangHelper """
    @classmethod
    def parse_from_body_request(cls, req):
        """ parse_from_body_request """
        if "body" not in req.context:
            raise NoBodyException()
        body = req.context["body"]

        penerimaan_barang = PenerimaanBarang()
        if "tanggal_terima" in body:
            penerimaan_barang.tanggal_terima = arrow.get(body["tanggal_terima"]).to("utc").datetime
        if "tanggal_entri" in body:
            penerimaan_barang.tanggal_entri = arrow.get(body["tanggal_entri"]).to("utc").datetime
        if "suplier" in body:
            penerimaan_barang.suplier = SuplierHelper.parse_from_dict(body["suplier"])
        if "user_entri" in body:
            penerimaan_barang.user_entri = UserHelper.parse_from_dict(body["user_entri"])
        if "user_cek" in body:
            penerimaan_barang.user_cek = UserHelper.parse_from_dict(body["user_cek"])
        if "list_barang" in body:
            for body_barang in body["list_barang"]:
                penerimaan_barang.list_barang.append(BarangHelper.parse_from_dict(body_barang))
        return penerimaan_barang

    @classmethod
    def parse_from_query_string_request(cls, req):
        penerimaan_barang = PenerimaanBarang()
        
        user_entri = req.get_param("user_entri") or None
        if user_entri is not None:
            penerimaan_barang.user_entri = User(id=user_entri)
        user_cek = req.get_param("user_cek") or None
        if user_cek is not None:
            penerimaan_barang.user_cek = User(id=user_cek)
        suplier = req.get_param("suplier") or None
        if suplier is not None:
            penerimaan_barang.suplier = Suplier(id=suplier)
        return penerimaan_barang

    @classmethod
    def parse_from_mongo_document(cls, document):
        """ parse_from_mongo_document """
        penerimaan_barang = PenerimaanBarang()
        penerimaan_barang.id = document["_id"]
        penerimaan_barang.tanggal_entri = arrow.get(document["tanggal_entri"]).to("utc").datetime
        penerimaan_barang.tanggal_terima = arrow.get(document["tanggal_terima"]).to("utc").datetime
        penerimaan_barang.user_cek = User(id=document["user_cek"]["id"])
        penerimaan_barang.user_entri = User(id=document["user_entri"]["id"])
        penerimaan_barang.suplier = Suplier(id=document["suplier"]["id"])

        for document_barang in document["list_barang"]:
            penerimaan_barang.list_barang.append(BarangHelper.parse_from_mongo_document(document_barang))
        return penerimaan_barang

    @classmethod
    def find(cls, penerimaan_barang, start_tanggal_entri, end_tanggal_entri, start_tanggal_terima, end_tanggal_terima):
        """ find """
        query = []
        if penerimaan_barang.user_entri is not None:
            query.append({"user_entri.id": {penerimaan_barang.user_entri.id}})
        if penerimaan_barang.user_cek is not None:
            query.append({"user_cek.id": {penerimaan_barang.user_cek.id}})
        if penerimaan_barang.suplier is not None:
            query.append({"suplier.id": {penerimaan_barang.suplier.id}})
        if start_tanggal_entri is not None:
            tanggal_entri_query = []
            tanggal_entri_query.append({"tanggal_entri": {"$gte": arrow.get(start_tanggal_entri).to("utc").datetime}})
            if end_tanggal_entri is not None:
                tanggal_entri_query.append({"tanggal_entri": {"$lte": arrow.get(end_tanggal_entri).to("utc").datetime}})
            query.append({"$and": tanggal_entri_query})
        if start_tanggal_terima is not None:
            tanggal_terima_query = []
            tanggal_terima_query.append({"tanggal_terima": {"$gte": arrow.get(start_tanggal_terima).to("utc").datetime}})
            if end_tanggal_terima is not None:
                tanggal_terima_query.append({"tanggal_terima": {"$lte": arrow.get(end_tanggal_terima).to("utc").datetime}})
            query.append({"$and": tanggal_terima_query})
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra
        documents = database.penerimaan_barang.find({"$and": query})
        list_penerimaan_barang = [PenerimaanBarangHelper.parse_from_mongo_document(document) for document in documents]
        client.close()
        return list_penerimaan_barang

    @classmethod
    def save(cls, penerimaan_barang):
        """ save """
        penerimaan_barang.tanggal_entri = arrow.utcnow().datetime

        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra
        result = database.penerimaan_barang.insert_one(penerimaan_barang.to_dict())

        for barang in penerimaan_barang.list_barang:
            database.barang.update_one({"barcode": barang.barcode}, {"$inc": {"stock": barang.stock}})
        client.close()
        return result.inserted_id

    @classmethod
    def get_detail(cls, penerimaan_barang):
        """ get_detail """
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra
        document = database.penerimaan_barang.find_one({"_id": ObjectId(penerimaan_barang.id)})
        penerimaan_barang = PenerimaanBarangHelper.parse_from_mongo_document(document)
        client.close()
        return penerimaan_barang
