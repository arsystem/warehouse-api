class Barang:
    def __init__(self, **kwargs):
        self.nama = kwargs.get("nama", None)
        self.barcode = kwargs.get("barcode", None)
        self.stock = kwargs.get("stock", None)

    def to_dict(self):
        return {
            "nama": self.nama,
            "barcode": self.barcode,
            "stock": int(self.stock)
        }