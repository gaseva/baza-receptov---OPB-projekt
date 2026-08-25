from presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user
import os
from services.sladice_service import SladiceService

ss = SladiceService()

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

@get('/')
def domaca_stran():
    return template("domaca_stran.html")


@get('/prijava')
def prijava():
    return template("prijava.html")

#@get('/seznam_receptov')
#def seznam_receptov():
#    return template("seznam_receptov.html")


@get("/recepti")
def seznam_receptov():
    sladice = ss.dobi_vse_sladice()

    return template(
        "seznam_receptov.html",
        sladice=sladice
    )

run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)