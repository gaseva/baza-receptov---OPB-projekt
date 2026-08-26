from presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user
import os
from services.sladice_service import SladiceService
from services.uporabniki_service import UporabnikiService

ss = SladiceService()
us = UporabnikiService()

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



@post('/registracija')
def registracija_post():
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    elektronski_naslov = request.forms.get('elektronski_naslov')
    uporabnisko_ime = request.forms.get('uporabnisko_ime')
    geslo = request.forms.get('geslo')
    ponovno_geslo = request.forms.get('ponovno_geslo')

    if geslo != ponovno_geslo:
        return template(
            'registracija.html',
            napaka='Gesli se ne ujemata.'
        )

    try:
        us.registracija(
            ime,
            priimek,
            elektronski_naslov,
            uporabnisko_ime,
            geslo
        )
    except ValueError as napaka:
        return template(
            'registracija.html',
            napaka=str(napaka)
        )

    redirect('/prijava')

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
    sestavine = ss.dobi_vse_sestavine()
    pripomocki = ss.dobi_vse_pripomocke()

    return template(
        "dodaj_recept.html",
        sestavine=sestavine,
        pripomocki=pripomocki,
        napaka_sestavine=None,
        napaka_pripomocka=None
    )


#post dodaj recept


@post("/dodaj_sestavino")
def dodaj_sestavino_post():
    ime = request.forms.get("ime_sestavine")
    enota = request.forms.get("enota_sestavine")

    try:
        ss.dodaj_sestavino(ime, enota)

    except ValueError as napaka:
        sestavine = ss.dobi_vse_sestavine()

        return template(
            "dodaj_recept.html",
            sestavine=sestavine,
            napaka_sestavine=str(napaka)
        )

    redirect("/dodaj_recept")


@post("/dodaj_pripomocek")
def dodaj_pripomocek_post():
    ime = request.forms.get("ime_pripomocka") # prebere ime iz obrazca

    try:
        ss.dodaj_pripomocek(ime)

    except ValueError as napaka:
        sestavine = ss.dobi_vse_sestavine()
        pripomocki = ss.dobi_vse_pripomocke()

        return template(
            "dodaj_recept.html",
            sestavine=sestavine,
            pripomocki=pripomocki,
            napaka_sestavine=None,
            napaka_pripomocka=str(napaka)
        )

    redirect("/dodaj_recept")


#@get("/priljubljene_recepti")
#def priljubljeni_recepti():
#    priljubljeno = ss.dobi_priljubljene_recepte()
#    return template("priljubljeni_recepti.html", priljubljeno=priljubljeno)


run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)