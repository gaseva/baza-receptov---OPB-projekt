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


#@post('/registracija')
#def registracija_post():
#    ime = request.forms.get('ime')
#    priimek = request.forms.get('priimek')
#    elektronski_naslov = request.forms.get('elektronski_naslov')
#    uporabnisko_ime = request.forms.get('uporabnisko_ime')
#    geslo = request.forms.get('geslo')
#    ponovno_geslo = request.forms.get('ponovno_geslo')
#
#    if geslo != ponovno_geslo:
#        return template(
#            'registracija.html',
#            napaka='Gesli se ne ujemata.'
#        )
#
#    try:
#        auth_service.registriraj_uporabnika(
#            ime,
#            priimek,
#            elektronski_naslov,
#            uporabnisko_ime,
#            geslo
#        )
#    except ValueError as napaka:
#        return template(
#            'registracija.html',
#            napaka=str(napaka)
#        )
#
#    redirect('/prijava')

@get("/recepti")
def seznam_receptov():
    sladice = ss.dobi_vse_sladice()

    return template(
        "seznam_receptov.html",
        sladice=sladice
    )

@get("/recepti/iskanje")
def seznam_receptov():
    iskanje = request.query.get("iskanje", "").strip()
    sladice = ss.poisci_sladice(iskanje)

    return template(
        "seznam_receptov.html",
        sladice=sladice,
        iskanje=iskanje
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


@get("/dodaj_recept")
def dodaj_recept():
    return template("dodaj_recept.html")


#@get("/priljubljene_recepti")
#def priljubljeni_recepti():
#    priljubljeno = ss.dobi_priljubljene_recepte()
#    return template("priljubljeni_recepti.html", priljubljeno=priljubljeno)


run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)