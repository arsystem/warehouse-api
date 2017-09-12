""" user.py """
import re

import pymongo
import arrow

from lib.model.user import User
from lib.exception import NoBodyException
from lib.config import Config

class UserHelper:
    """ UserHelper """
    @classmethod
    def parse_from_dict(cls, data):
        """ parse_from_dict """
        user = User()
        if "id" in data:
            user.id = data["id"]
        if "nama" in data:
            user.nama = data["nama"]
        if "password" in data:
            user.password = data["password"]
        return user

    @classmethod
    def parse_from_body_request(cls, req):
        """ parse_from_body_request """
        if "body" not in req.context:
            raise NoBodyException()
        body = req.context["body"]
        return UserHelper.parse_from_dict(body)

    @classmethod
    def parse_from_mongo_document(cls, document):
        """ parse_from_mongo_document """
        if document is not None:
            user = User()
            user.id = document["id"]
            user.nama = document["nama"]
            user.password = document["password"]
            return user
        return None

    @classmethod
    def parse_from_query_string_request(cls, req):
        """ parse_from_query_string_request """
        user = User()
        user.id = req.get_param("id") or None
        user.nama = req.get_param("nama") or None
        user.password = req.get_param("password") or None
        return user

    @classmethod
    def find(cls, user):
        """ find """
        query = []
        if user.id is not None:
            query.append({"id": re.compile(user.id, re.IGNORECASE)})
        if user.nama is not None:
            query.append({"nama": re.compile(user.nama, re.IGNORECASE)})

        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra
        if len(query) > 0:
            documents = database.user.find({"$or": query})
        else:
            documents = database.user.find({})
        list_user = [UserHelper.parse_from_mongo_document(document) for document in documents]
        client.close()

        return list_user

    @classmethod
    def save(cls, user):
        """ save """
        document = UserHelper.get_detail(user)

        if document is None:
            client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
            database = client.tokosumatra
            inserted_id = database.user.insert_one(user.to_dict())
            client.close()
            return inserted_id
        return user.id

    @classmethod
    def get_detail(cls, user):
        """ get_detail """
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra
        document = database.user.find_one({"id": user.id})
        client.close()

        return UserHelper.parse_from_mongo_document(document)

    @classmethod
    def delete(cls, user):
        """ delete """
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        source_database = client.tokosumatra
        delete_database = client.trash_tokosumatra

        document = UserHelper.get_detail(user).to_dict()
        document.update({"deleted_at": arrow.utcnow().datetime})

        delete_database.user.insert_one(document)
        source_database.user.delete_one({"id": user.id})
        client.close()

    @classmethod
    def update(cls, user):
        """ update """
        update_fields = {}
        if user.nama is not None:
            update_fields.update({"nama": user.nama})
        if user.password is not None:
            update_fields.update({"password": user.password})

        if len(update_fields) > 0:
            client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
            database = client.tokosumatra
            database.user.update({"id": user.id}, {"$set": update_fields})
            client.close()

    @classmethod
    def login(cls, user):
        """ login """
        if not user.id and not user.password:
            return False

        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra
        document = database.user.find({"$and": [
            {"id": user.id},
            {"password": user.password}
        ]})
        if document is None or document.count() == 0:
            return False
        return True