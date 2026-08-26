from presentation.bottleext import get, post, run, request, template, redirect, static_file, url, response, template_user
import os
from services.sladice_service import SladiceService
from services.uporabniki_service import UporabnikiService
from functools import wraps
import secrets
import json
from urllib.parse import urlencode

ss = SladiceService()
us = UporabnikiService()

# privzete nastavitve
SERVER_PORT = os.environ.get('BOTTLE_PORT', 8080)
RELOADER = os.environ.get('BOTTLE_RELOADER', True)

COOKIE_SECRET = (
    os.environ.get("COOKIE_SECRET")
    or secrets.token_urlsafe(32)
)

if not COOKIE_SECRET:
    raise RuntimeError(
        "cookie_secret ni nastavljen v auth_private.py."
    )

def dobi_prijavljeno_osebo_id():
    """Vrne ID prijavljenega uporabnika ali None."""

    oseba_id = request.get_cookie(
        "oseba_id",
        secret=COOKIE_SECRET
    )

    if oseba_id is None:
        return None

    try:
        return int(oseba_id)
    except (TypeError, ValueError):
        return None

    

def cookie_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        oseba_id = dobi_prijavljeno_osebo_id()

        if oseba_id is None:
            return redirect("/prijava")

        return f(*args, **kwargs)

    return decorated

@get("/")
def domaca_stran():
    oseba_id = dobi_prijavljeno_osebo_id()
    kategorije = ss.dobi_kategorije()

    return template(
        "domaca_stran.html",
        prijavljen=oseba_id is not None,
        kategorije=kategorije
    )


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
    return template(
        "registracija.html",
        podatki={}
    )

@post('/registracija')
def registracija_post():
    ime = request.forms.get('ime')
    priimek = request.forms.get('priimek')
    elektronski_naslov = request.forms.get('elektronski_naslov')
    uporabnisko_ime = request.forms.get('uporabnisko_ime')
    geslo = request.forms.get('geslo')
    ponovno_geslo = request.forms.get('ponovno_geslo')

    # Ob napaki ohranimo nesenzitivne podatke. Gesel zaradi varnosti
    # nikoli ne pošiljamo nazaj v HTML.
    podatki = {
        "ime": (ime or "").strip(),
        "priimek": (priimek or "").strip(),
        "elektronski_naslov": (elektronski_naslov or "").strip(),
        "uporabnisko_ime": (uporabnisko_ime or "").strip(),
    }
    
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
            podatki=podatki,
        )

    
    if len(geslo) < 8:
        return template(
            'registracija.html',
            napaka='Geslo mora vsebovati najmanj 8 znakov.',
            podatki=podatki,
        )

    if geslo != ponovno_geslo:
        return template(
            'registracija.html',
            napaka='Gesli se ne ujemata.',
            podatki=podatki,
        )

    try:
        oseba_id = us.registracija(
            ime,
            priimek,
            elektronski_naslov,
            uporabnisko_ime,
            geslo
        )
    except ValueError as napaka:
        return template(
            'registracija.html',
            napaka=str(napaka),
            podatki=podatki,
        )
    
    response.set_cookie(
        "oseba_id",
        str(oseba_id),
        secret=COOKIE_SECRET,
        httponly=True,
        samesite="Lax",
        secure=False,
        path="/",
        )

    return redirect('/')

@get("/odjava")
def odjava():
    response.delete_cookie(
        "oseba_id",
        path="/",
    )
    return redirect("/")

@get("/recepti")
def seznam_receptov():
    oseba_id = dobi_prijavljeno_osebo_id()
    sladice = ss.dobi_vse_sladice()

    if oseba_id is None:
        priljubljeni_idji = set()
    else:
        priljubljeni_idji = (
            us.dobi_id_priljubljenih_receptov(oseba_id)
        )

    return template(
        "seznam_receptov.html",
        sladice=sladice,
        iskanje="",
        priljubljeni_idji=priljubljeni_idji,
    )

@get("/recepti/iskanje")
def iskanje_receptov():
    iskanje = request.query.get(
        "iskanje",
        ""
    ).strip()

    kategorija_id = request.query.get(
        "kategorija",
        ""
    ).strip()

    sladice = ss.poisci_sladice(
        iskanje,
        kategorija_id,
    )

    oseba_id = dobi_prijavljeno_osebo_id()

    if oseba_id is None:
        priljubljeni_idji = set()
    else:
        priljubljeni_idji = (
            us.dobi_id_priljubljenih_receptov(oseba_id)
        )

    return template(
        "seznam_receptov.html",
        sladice=sladice,
        iskanje=iskanje,
        priljubljeni_idji=priljubljeni_idji,
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
@cookie_required
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
@cookie_required
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
    avtor_id = dobi_prijavljeno_osebo_id()

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
@cookie_required
def dodaj_sestavino_post():
    ime = request.forms.get("ime_sestavine")
    enota = request.forms.get("enota_sestavine")

    try:
        sestavina = ss.dodaj_sestavino(ime, enota)

    except ValueError as napaka:
        response.status = 400
        response.content_type = "application/json"
        return json.dumps(
            {
                "uspeh": False,
                "napaka": str(napaka),
            },
            ensure_ascii=False,
        )

    response.content_type = "application/json"
    return json.dumps(
        {
            "uspeh": True,
            "sestavina": {
                "id": sestavina.id,
                "ime": sestavina.ime,
                "enota": sestavina.enota,
            },
        },
        ensure_ascii=False,
    )


@post("/dodaj_pripomocek")
@cookie_required
def dodaj_pripomocek_post():
    ime = request.forms.get("ime_pripomocka") # prebere ime iz obrazca

    try:
        pripomocek = ss.dodaj_pripomocek(ime)

    except ValueError as napaka:
        response.status = 400
        response.content_type = "application/json"
        return json.dumps(
            {
                "uspeh": False,
                "napaka": str(napaka),
            },
            ensure_ascii=False,
        )

    response.content_type = "application/json"
    return json.dumps(
        {
            "uspeh": True,
            "pripomocek": {
                "id": pripomocek.id,
                "ime": pripomocek.ime,
            },
        },
        ensure_ascii=False,
    )


@get("/priljubljeni_recepti")
@cookie_required
def priljubljeni_recepti():
    oseba_id = dobi_prijavljeno_osebo_id()
    priljubljeno = us.priljubljeni_recepti(oseba_id)
    return template("priljubljeni_recepti.html", priljubljeno=priljubljeno)

@post("/priljubljeni/dodaj/<sladica_id:int>")
@cookie_required
def dodaj_med_priljubljene(sladica_id):
    oseba_id = dobi_prijavljeno_osebo_id()

    us.dodaj_med_priljubljene(
        oseba_id,
        sladica_id
    )

    return redirect("/recepti")

@post("/priljubljeni/preklopi/<sladica_id:int>")
@cookie_required
def preklopi_priljubljeni_recept(sladica_id):
    oseba_id = dobi_prijavljeno_osebo_id()

    try:
        us.preklopi_priljubljeni_recept(
            oseba_id,
            sladica_id
        )
    except ValueError as napaka:
        response.status = 404
        return template(
            "napaka.html",
            napaka=str(napaka)
        )

    iskanje = request.forms.get("iskanje", "").strip()

    if iskanje:
        parametri = urlencode({"iskanje": iskanje})
        return redirect(f"/recepti/iskanje?{parametri}")

    return redirect("/recepti")

run(host='localhost', port=SERVER_PORT, reloader=RELOADER, debug=True)