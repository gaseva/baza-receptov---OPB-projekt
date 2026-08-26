from presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user
import os
from services.sladice_service import SladiceService
from services.uporabniki_service import UporabnikiService
from functools import wraps
from data import auth_private as auth

ss = SladiceService()
us = UporabnikiService()

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

COOKIE_SECRET = auth.cookie_secret
if not COOKIE_SECRET:
    raise RuntimeError(
        "Okoljska spremenljivka COOKIE_SECRET ni nastavljena."
    )

def cookie_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        oseba_id = request.get_cookie("oseba_id", secret=COOKIE_SECRET)

        if oseba_id is None:
            return redirect("/prijava")

        try:
            int(oseba_id)
        except (TypeError, ValueError):
            return redirect("/prijava")

        return f(*args, **kwargs)

    return decorated

@get('/')
def domaca_stran():
    return template("domaca_stran.html")


@get('/prijava')
def prijava():
    return template("prijava.html")

@post('/prijava')
def prijava_post():
    uporabnisko_ime = request.forms.get('username')
    geslo = request.forms.get('password')
    
    if not uporabnisko_ime or not geslo:
        return template(
            "prijava.html",
            napaka="Prosim izpolnite vsa polja."
        )
        
    try:
        uporabnik = us.prijava(
            uporabnisko_ime,
            geslo
        )
    except ValueError as napaka:
        return template(
            'prijava.html',
            napaka=str(napaka)
        )
    
    response.set_cookie(
        "oseba_id",
        str(uporabnik.id),
        secret=COOKIE_SECRET,
        httponly=True,
        samesite="Lax",
        secure=False,
        path="/",
    )

    return redirect('/')




@get("/registracija", name="registracija")
def registracija():
    return template("registracija.html")

@post('/registracija')
def registracija_post():
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    elektronski_naslov = request.forms.get('elektronski_naslov')
    uporabnisko_ime = request.forms.get('uporabnisko_ime')
    geslo = request.forms.get('geslo')
    ponovno_geslo = request.forms.get('ponovno_geslo')
    
    if not all([
        ime,
        priimek,
        elektronski_naslov,
        uporabnisko_ime,
        geslo,
        ponovno_geslo,
    ]):
        return template(
            "registracija.html",
            napaka="Prosim, izpolnite vsa polja.",
        )

    
    if len(geslo) < 8:
        return template(
            'registracija.html',
            napaka='Geslo mora vsebovati najmanj 8 znakov.'
        )

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

    return redirect('/prijava')

@get("/odjava")
def odjava():
    response.delete_cookie(
        "oseba_id",
        path="/",
    )
    return redirect("/")

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
        napaka_pripomocka=None,
        napaka_recepta=None
    )


@post("/dodaj_recept")
def dodaj_recept_post():
    ime = request.forms.get("ime")
    cas_priprave = request.forms.get("cas_priprave")
    tezavnost_id = request.forms.get("tezavnost")
    kategorija_id = request.forms.get("kategorija")
    kratek_opis = request.forms.get("kratek_opis")
    postopek = request.forms.get("postopek")

    sestavina_ids = request.forms.getall("sestavine")
    kolicine = request.forms.getall("kolicina")
    pripomocek_ids = request.forms.getall("pripomocki")

    # Začasno, dokler prijava uporabnika še ni povezana z dodajanjem recepta.
    # Pozneje bo tukaj ID trenutno prijavljenega uporabnika iz piškotka/seje.
    avtor_id = 1

    try:
        sladica_id = ss.dodaj_sladico(
            ime=ime,
            cas_priprave=cas_priprave,
            postopek=postopek,
            kratek_opis=kratek_opis,
            avtor_id=avtor_id,
            tezavnost_id=tezavnost_id,
            kategorija_id=kategorija_id,
            sestavina_ids=sestavina_ids,
            kolicine=kolicine,
            pripomocek_ids=pripomocek_ids,
        )

    except ValueError as napaka:
        sestavine = ss.dobi_vse_sestavine()
        pripomocki = ss.dobi_vse_pripomocke()

        return template(
            "dodaj_recept.html",
            sestavine=sestavine,
            pripomocki=pripomocki,
            napaka_sestavine=None,
            napaka_pripomocka=None,
            napaka_recepta=str(napaka)
        )

    redirect(f"/recept/{sladica_id}")




@post("/dodaj_sestavino")
def dodaj_sestavino_post():
    ime = request.forms.get("ime_sestavine")
    enota = request.forms.get("enota_sestavine")

    try:
        ss.dodaj_sestavino(ime, enota)

    except ValueError as napaka:
        sestavine = ss.dobi_vse_sestavine()
        pripomocki = ss.dobi_vse_pripomocke()

        return template(
            "dodaj_recept.html",
            sestavine=sestavine,
            pripomocki=pripomocki,
            napaka_sestavine=str(napaka),
            napaka_pripomocka=None,
            napaka_recepta=None
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
            napaka_pripomocka=str(napaka),
            napaka_recepta=None
        )

    redirect("/dodaj_recept")


#@get("/priljubljene_recepti")
#def priljubljeni_recepti():
#    priljubljeno = ss.dobi_priljubljene_recepte()
#    return template("priljubljeni_recepti.html", priljubljeno=priljubljeno)


run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)