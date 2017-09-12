""" Main program runs here """
import logging

import falcon

from falcon_cors import CORS
from waitress import serve

from lib.listener.barang import ListBarangListener, BarangListener
from lib.listener.suplier import ListSuplierListener, SuplierListener
from lib.listener.user import ListUserListener, UserListener
from lib.listener.login import LoginListener
from lib.listener.customer import ListCustomerListener, CustomerListener
from lib.listener.pengambilan_barang import ListPengambilanBarangListener, PengambilanBarangListener
from lib.listener.penerimaan_barang import ListPenerimaanBarangListener, PenerimaanBarangListener
from lib.middleware import RequireJSON, JSONTranslator

def run():
    """ Main program runs here """
    cors = CORS(
        allow_all_origins=True,
        allow_all_headers=True,
        allow_all_methods=True
    )

    app = falcon.API(middleware=[
        cors.middleware,
        RequireJSON(),
        JSONTranslator()
    ])

    app.add_route("/barang", ListBarangListener())
    app.add_route("/barang/{barcode}", BarangListener())
    app.add_route("/suplier", ListSuplierListener())
    app.add_route("/suplier/{_id}", SuplierListener())
    app.add_route("/user", ListUserListener())
    app.add_route("/user/{_id}", UserListener())
    app.add_route("/customer", ListCustomerListener())
    app.add_route("/customer/{_id}", CustomerListener())
    app.add_route("/pengambilan_barang", ListPengambilanBarangListener())
    app.add_route("/pengambilan_barang/{_id}", PengambilanBarangListener())
    app.add_route("/penerimaan_barang", ListPenerimaanBarangListener())
    app.add_route("/penerimaan_barang/{_id}", PenerimaanBarangListener())
    app.add_route("/login", LoginListener())

    serve(app, host="0.0.0.0", port=8080, threads=100, asyncore_use_poll=True)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    run()
