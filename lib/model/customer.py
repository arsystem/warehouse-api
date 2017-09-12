""" customer.py """
class Customer:
    """ Customer """
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.nama = kwargs.get("nama", None)

    def to_dict(self):
        """ to_dict """
        return {
            "id": self.id,
            "nama": self.nama
        }