""" suplier.py """
import re

import pymongo
import arrow

from lib.model.suplier import Suplier
from lib.exception import NoBodyException
from lib.config import Config

class SuplierHelper:
    """ SuplierHelper """

    @classmethod
    def parse_from_mongo_document(cls, document):
        """ parse_from_mongo_document """
        if document is not None:
            suplier = Suplier()
            suplier.id = document["id"]
            suplier.nama = document["nama"]
            return suplier
        return None

    @classmethod
    def parse_from_dict(cls, data):
        """ parse_from_dict """
        suplier = Suplier()
        if "nama" in data:
            suplier.nama = data["nama"]
        if "id" in data:
            suplier.id = data["id"]
        return suplier

    @classmethod
    def parse_from_body_request(cls, req):
        """ parse_from_body_request """
        if "body" not in req.context:
            raise NoBodyException()
        body = req.context["body"]
        return SuplierHelper.parse_from_dict(body)

    @classmethod
    def parse_from_query_string_request(cls, req):
        """ parse_from_query_string_request """
        suplier = Suplier()
        suplier.id = req.get_param("id") or None
        suplier.nama = req.get_param("nama") or None
        return suplier

    @classmethod
    def save(cls, suplier):
        """ save """
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra
        inserted_id = database.suplier.insert_one(suplier.to_dict())
        client.close()
        return inserted_id

    @classmethod
    def find(cls, suplier):
        """ find """
        query = []
        if suplier.nama is not None:
            query.append({"nama": re.compile(suplier.nama, re.IGNORECASE)})
        if suplier.id is not None:
            query.append({"id": re.compile(suplier.id, re.IGNORECASE)})
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra

        if len(query) > 0:
            documents = database.suplier.find({"$or": query})
        else:
            documents = database.suplier.find({})
        list_suplier = [SuplierHelper.parse_from_mongo_document(document) for document in documents]
        client.close()
        return list_suplier

    @classmethod
    def get_detail(cls, suplier):
        """ get_detail """
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra
        document = database.suplier.find_one({"id": suplier.id})
        suplier = SuplierHelper.parse_from_mongo_document(document)
        client.close()
        return suplier

    @classmethod
    def delete(cls, suplier):
        """ delete """
        suplier = SuplierHelper.get_detail(suplier)

        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        source_database = client.tokosumatra
        delete_database = client.trash_tokosumatra

        document = suplier.to_dict()
        document.update({"deleted_time": arrow.utcnow().datetime})
        delete_database.suplier.insert_one(document)
        source_database.suplier.delete_one({"id": suplier.id})
        client.close()

    @classmethod
    def update(cls, suplier):
        """ update """
        update_fields = {}
        if suplier.nama is not None:
            update_fields.update({"nama": suplier.nama})

        if len(update_fields) > 0:
            client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
            database = client.tokosumatra
            database.suplier.update({"id": suplier.id}, {"$set": update_fields})
            client.close()
