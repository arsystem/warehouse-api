""" pengambilan_barang.py """
import arrow

class PengambilanBarang:
    """ PengambilanBarang """
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.tanggal_ambil = kwargs.get("tanggal_ambil", None)
        self.tanggal_entri = kwargs.get("tanggal_entri", None)
        self.list_barang = kwargs.get("list_barang", [])
        self.user_cek = kwargs.get("user_cek", None)
        self.user_entri = kwargs.get("user_entri", None)
        self.customer = kwargs.get("customer", None)

    def to_dict(self):
        """ to_dict """
        return {
            "id": self.id,
            "tanggal_ambil": arrow.get(self.tanggal_ambil).to("utc").datetime,
            "tanggal_entri": arrow.get(self.tanggal_entri).to("utc").datetime,
            "list_barang": [barang.to_dict() for barang in self.list_barang],
            "user_cek": self.user_cek.to_dict(),
            "user_entri": self.user_entri.to_dict(),
            "customer": self.customer.to_dict()
        }