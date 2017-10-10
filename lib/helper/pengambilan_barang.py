""" pengambilan_barang.py """
import pymongo
import arrow

from bson.objectid import ObjectId

from lib.model.pengambilan_barang import PengambilanBarang
from lib.model.user import User
from lib.model.customer import Customer
from lib.helper.user import UserHelper
from lib.helper.customer import CustomerHelper
from lib.helper.barang import BarangHelper
from lib.exception import NoBodyException
from lib.config import Config

class PengambilanBarangHelper:
    """ PengambilanBarangHelper """
    @classmethod
    def parse_from_mongo_document(cls, document):
        """ parse_from_mongo_document """
        pengambilan_barang = PengambilanBarang()
        pengambilan_barang.id = document["_id"]
        pengambilan_barang.tanggal_ambil = arrow.get(document["tanggal_ambil"]).to("utc").datetime
        pengambilan_barang.tanggal_entri = arrow.get(document["tanggal_entri"]).to("utc").datetime
        pengambilan_barang.user_cek = User(id=document["user_cek"]["id"])
        pengambilan_barang.user_entri = User(id=document["user_entri"]["id"])
        pengambilan_barang.customer = Customer(id=document["customer"]["id"])

        for barang_document in document["list_barang"]:
            pengambilan_barang.list_barang.append(BarangHelper.parse_from_mongo_document(barang_document))
        return pengambilan_barang

    @classmethod
    def parse_from_body_request(cls, req):
        """ parse_from_body_request """
        if "body" not in req.context:
            raise NoBodyException()
        body = req.context["body"]

        pengambilan_barang = PengambilanBarang()
        if "tanggal_ambil" in body:
            pengambilan_barang.tanggal_ambil = arrow.get(body["tanggal_ambil"]).to("utc").datetime
        if "tanggal_entri" in body:
            pengambilan_barang.tanggal_entri = arrow.get(body["tanggal_entri"]).to("utc").datetime
        if "user_entri" in body:
            pengambilan_barang.user_entri = UserHelper.parse_from_dict(body["user_entri"])
        if "user_cek" in body:
            pengambilan_barang.user_cek = UserHelper.parse_from_dict(body["user_cek"])
        if "customer" in body:
            pengambilan_barang.customer = CustomerHelper.parse_from_dict(body["customer"])
        if "list_barang" in body:
            for barang_body in body["list_barang"]:
                pengambilan_barang.list_barang.append(BarangHelper.parse_from_dict(barang_body))
        return pengambilan_barang

    @classmethod
    def parse_from_query_string(cls, req):
        """ parse_from_query_string """
        pengambilan_barang = PengambilanBarang()
        user_cek = req.get_param("user_cek") or None
        if user_cek is not None:
            pengambilan_barang.user_cek = User(id=user_cek)
        user_entri = req.get_param("user_entri") or None
        if user_entri is not None:
            pengambilan_barang.user_entri = User(id=user_entri)
        customer = req.get_param("customer") or None
        if customer is not None:
            pengambilan_barang.customer = Customer(id=customer)
        return pengambilan_barang

    @classmethod
    def save(cls, pengambilan_barang):
        """ save """
        pengambilan_barang.tanggal_entri = arrow.utcnow().datetime

        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra
        result = database.pengambilan_barang.insert_one(pengambilan_barang.to_dict())
        for barang in pengambilan_barang.list_barang:
            database.barang.update_one({"barcode": barang.barcode}, {"$inc": {"stock": (-1 * barang.stock)}})
        client.close()
        return result.inserted_id

    @classmethod
    def find(cls, pengambilan_barang, start_tanggal_entri, end_tanggal_entri, start_tanggal_ambil, end_tanggal_ambil):
        """ find """
        query = []
        if pengambilan_barang.user_cek is not None:
            query.append({"user_cek.id": pengambilan_barang.user_cek.id})
        if pengambilan_barang.user_entri is not None:
            query.append({"user_entri.id": pengambilan_barang.user_entri.id})
        if pengambilan_barang.customer is not None:
            query.append({"customer.id": pengambilan_barang.customer.id})
        if start_tanggal_entri is not None:
            tanggal_entri_query = []
            tanggal_entri_query.append({"tanggal_entri": {"$gte": arrow.get(start_tanggal_entri).to("utc").datetime}})
            if end_tanggal_entri is not None:
                tanggal_entri_query.append({"tanggal_entri": {"$lte": arrow.get(end_tanggal_entri).to("utc").datetime}})
            query.append({"$and": tanggal_entri_query})
        if start_tanggal_ambil is not None:
            tanggal_ambil_query = []
            tanggal_ambil_query.append({"tanggal_ambil": {"$gte": arrow.get(start_tanggal_ambil).to("utc").datetime}})
            if end_tanggal_ambil is not None:
                tanggal_ambil_query.append({"tanggal_ambil": {"$lte": arrow.get(end_tanggal_ambil).to("utc").datetime}})
            query.append({"$and": tanggal_ambil_query})
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra

        if len(query) == 0:
            documents = database.pengambilan_barang.find({})
        else:
            documents = database.pengambilan_barang.find({"$and": query})

        list_pengambilan_barang = [PengambilanBarangHelper.parse_from_mongo_document(document) for document in documents]
        client.close()
        return list_pengambilan_barang

    @classmethod
    def get_detail(cls, pengambilan_barang):
        """ get_detail """
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra
        document = database.pengambilan_barang.find_one({"_id": ObjectId(pengambilan_barang.id)})
        pengambilan_barang = PengambilanBarangHelper.parse_from_mongo_document(document)
        client.close()
        return pengambilan_barang