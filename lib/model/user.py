""" user.py """
class User:
    """ User """
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.nama = kwargs.get("nama", None)
        self.password = kwargs.get("password", None)

    def to_dict(self):
        """ to_dict """
        return {
            "id": self.id,
            "nama": self.nama,
            "password": self.password
        }