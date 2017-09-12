""" customer.py """
import falcon

from lib.model.customer import Customer
from lib.helper.customer import CustomerHelper

class ListCustomerListener:
    """ ListCustomerListener """
    def on_post(self, req, res):
        """ handle POST requests """
        customer = CustomerHelper.parse_from_body_request(req)
        CustomerHelper.save(customer)
        req.context["result"] = {"status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

    def on_get(self, req, res):
        """ handle GET requests """
        customer = CustomerHelper.parse_from_query_string_request(req)
        list_customer = CustomerHelper.find(customer)
        req.context["result"] = {"data": [customer.to_dict() for customer in list_customer], "status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

class CustomerListener:
    """ CustomerListner """
    def on_get(self, req, res, _id):
        """ handle GET requests """
        customer = Customer()
        customer.id = _id
        customer = CustomerHelper.get_detail(customer)
        req.context["result"] = {"data": customer.to_dict(), "status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

    def on_delete(self, req, res, _id):
        """ handle DELETE requests """
        customer = Customer()
        customer.id = _id
        CustomerHelper.delete(customer)
        req.context["result"] = {"status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200

    def on_put(self, req, res, _id):
        """ handle PUT requests """
        customer = CustomerHelper.parse_from_query_string_request(req)
        customer.id = _id
        CustomerHelper.update(customer)
        req.context["result"] = {"status": {"code": 200, "message": "success"}}
        res.status = falcon.HTTP_200
