""" barang.py """
import re

import pymongo
import arrow

from lib.model.barang import Barang
from lib.exception import NoBodyException
from lib.config import Config

class BarangHelper:
    """ BarangHelper """
    @classmethod
    def parse_from_mongo_document(cls, document):
        """ parse_from_mongo_document """
        barang = Barang()
        barang.nama = document["nama"]
        barang.barcode = document["barcode"]
        barang.stock = int(document["stock"])
        return barang

    @classmethod
    def parse_from_dict(cls, data):
        """ parse_from_dict """
        barang = Barang()
        if "nama" in data:
            barang.nama = data["nama"]
        if "barcode" in data:
            barang.barcode = data["barcode"]
        if "stock" in data:
            barang.stock = int(data["stock"])
        return barang

    @classmethod
    def parse_from_body_request(cls, req):
        """ parse_from_body_request """
        if "body" not in req.context:
            raise NoBodyException()
        body = req.context["body"]
        return BarangHelper.parse_from_dict(body)

    @classmethod
    def parse_from_query_string_request(cls, req):
        """ parse_from_query_string_request """
        barang = Barang()
        barang.barcode = req.get_param("barcode") or None
        barang.nama = req.get_param("nama") or None
        return barang

    @classmethod
    def save(cls, barang):
        """ save """
        if not barang.nama and not barang.barcode and not barang.stock:
            return False
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra
        inserted_id = database.barang.insert_one(barang.to_dict())
        client.close()
        return inserted_id

    @classmethod
    def find(cls, barang):
        """ find """
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra
        query = []
        if barang.nama is not None:
            query.append({"nama": re.compile(barang.nama, re.IGNORECASE)})
        if barang.barcode is not None:
            query.append({"barcode": re.compile(barang.barcode, re.IGNORECASE)})
        if len(query) > 0:
            documents = database.barang.find({"$or": query})
        else:
            documents = database.barang.find({})
        list_barang = [BarangHelper.parse_from_mongo_document(document) for document in documents]
        client.close()
        return list_barang

    @classmethod
    def get_detail(cls, barang):
        """ get_detail """
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra
        document = database.barang.find_one({"barcode": barang.barcode})

        if document is not None:
            barang = BarangHelper.parse_from_mongo_document(document)
            client.close()
            return barang
        return False

    @classmethod
    def delete(cls, barang):
        """ delete """
        barang = BarangHelper.get_detail(barang)

        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        source_database = client.tokosumatra
        delete_database = client.trash_tokosumatra
        source_database.barang.delete_one({"barcode": baracode})

        document = barang.to_dict()
        document.update({"deleted_time": arrow.utcnow().datetime})
        delete_database.barang.insert_one(document)

    @classmethod
    def update(cls, barang):
        """ update """
        update_fields = {}
        if barang.barcode is not None:
            update_fields.update({"barcode": barang.barcode})
        if barang.nama is not None:
            update_fields.update({"nama": barang.nama})
        if barang.stock is not None:
            update_fields.update({"stock": int(barang.stock)})

        if len(update_fields) > 0:
            client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
            database = client.tokosumatra
            database.barang.update({"barcode": barang.barcode}, {"$set": update_fields})
            client.close()