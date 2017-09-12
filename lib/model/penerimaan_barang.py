""" penerimaan_barang.py """
import arrow

class PenerimaanBarang:
    """ PenerimaanBarang """
    def __init__(self, **kwargs):
        self.id = kwargs.get("id", None)
        self.tanggal_terima = kwargs.get("tanggal_terima", None)
        self.tanggal_entri = kwargs.get("tanggal_entri", None)
        self.list_barang = kwargs.get("list_barang", [])
        self.suplier = kwargs.get("suplier", None)
        self.user_entri = kwargs.get("user_entri", None)
        self.user_cek = kwargs.get("user_cek", None)

    def to_dict(self):
        return {
            "id": self.id,
            "tanggal_terima": arrow.get(self.tanggal_terima).to("utc").datetime,
            "tanggal_entri": arrow.get(self.tanggal_entri).to("utc").datetime,
            "list_barang": [barang.to_dict() for barang in self.list_barang],
            "suplier": self.suplier.to_dict(),
            "user_entri": self.user_entri.to_dict(),
            "user_cek": self.user_cek.to_dict()
        }