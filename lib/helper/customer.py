""" customer.py """
import re

import pymongo
import arrow

from lib.model.customer import Customer
from lib.exception import NoBodyException
from lib.config import Config

class CustomerHelper:
    """ CustomerHelper """
    @classmethod
    def parse_from_mongo_document(cls, document):
        """ parse_from_mongo_document """
        if document is not None:
            customer = Customer()
            customer.id = document["id"]
            customer.nama = document["nama"]
            return customer
        return None

    @classmethod
    def parse_from_dict(cls, data):
        """ parse_from_dict """
        customer = Customer()
        if "id" in data:
            customer.id = data["id"]
        if "nama" in data:
            customer.nama = data["nama"]
        return customer

    @classmethod
    def parse_from_body_request(cls, req):
        """ parse_from_body_request """
        if "body" not in req.context:
            raise NoBodyException()
        body = req.context["body"]
        return CustomerHelper.parse_from_dict(body)

    @classmethod
    def parse_from_query_string_request(cls, req):
        """ parse_from_query_string_request """
        customer = Customer()
        customer.id = req.get_param("id") or None
        customer.nama = req.get_param("nama") or None
        return customer

    @classmethod
    def save(cls, customer):
        """ save """
        document = CustomerHelper.get_detail(customer)
        if document is None:
            client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
            database = client.tokosumatra
            inserted_id = database.customer.insert_one(customer.to_dict())
            client.close()
            return inserted_id
        return customer.id

    @classmethod
    def find(cls, customer):
        """ find """
        query = []
        if customer.id is not None:
            query.append({"id": re.compile(customer.id, re.IGNORECASE)})
        if customer.nama is not None:
            query.append({"nama": re.compile(customer.nama, re.IGNORECASE)})
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra

        if len(query) > 0:
            documents = database.customer.find({"$and": query})
        else:
            documents = database.customer.find({})
        list_customer = [CustomerHelper.parse_from_mongo_document(document) for document in documents]
        client.close()
        return list_customer

    @classmethod
    def get_detail(cls, customer):
        """ get_detail """
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        database = client.tokosumatra
        document = database.customer.find_one({"id": customer.id})
        customer = CustomerHelper.parse_from_mongo_document(document)
        client.close()
        return customer

    @classmethod
    def delete(cls, customer):
        """ delete """
        client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
        source_database = client.tokosumatra
        delete_database = client.trash_tokosumatra

        document = CustomerHelper.get_detail(customer).to_dict()
        document.update({"deleted_at": arrow.utcnow().datetime})
        delete_database.customer.insert_one(document)
        source_database.customer.delete_one({"id": customer.id})
        client.close()

    @classmethod
    def update(cls, customer):
        """ update """
        update_fields = {}
        if customer.nama is not None:
            update_fields.update({"nama": customer.nama})
        if len(update_fields) > 0:
            client = pymongo.MongoClient(Config.DATABASE_ADDRESS)
            database = client.tokosumatra
            database.customer.update({"id": customer.id}, {"$set": update_fields})
            client.close()
