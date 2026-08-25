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

#@post('/prijava')
#def prijava_post():
#    uporabnisko_ime = request.forms.get('username')
#    geslo = request.forms.get('password')


@get('/registracija')
def registracija():
    return template("registracija.html")



@get("/recepti")
def seznam_receptov():
    sladice = ss.dobi_vse_sladice()

    return template(
        "seznam_receptov.html",
        sladice=sladice#,
        #iskanje = ""
    )

@get("/recept/<sladica_id:int>")
def recept(sladica_id):
    sladica, sestavine = ss.dobi_recept(sladica_id)

    if sladica is None:
        response.status = 404
        return template(
            "napaka.html",
            napaka="Sladica s tem ID-jem ne obstaja."
        )

    return template(
        "recept.html",
        sladica=sladica,
        sestavine=sestavine
    )

run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)