"""Podatkovni razredi, ki jih uporablja aplikacija.

Razredi v tej datoteki samo opisujejo obliko podatkov. Ne odpirajo povezave
z bazo in ne izvajajo SQL-poizvedb; za to skrbi razred Repository.
"""

from dataclasses import dataclass


@dataclass
class Oseba:
    """Uporabnik aplikacije oziroma ena vrstica tabele oseba."""

    id: int
    ime: str
    priimek: str
    elektronski_naslov: str
    uporabnisko_ime: str
    geslo_hash: str
    role: str

@dataclass
class Tezavnost:
    """Stopnja težavnosti priprave sladice."""

    id: int
    tezavnost: str
    
    
@dataclass
class Kategorija:
    """Kategorija sladice, na primer torta ali piškoti."""

    id: int
    ime: str


@dataclass
class Sladica:
    """Sladica z berljivimi podatki za prikaz v spletni predlogi.

    Poleg osnovnih podatkov vsebuje ID-je in imena povezanega avtorja,
    težavnosti ter kategorije. Te vrednosti Repository pridobi z JOIN-i.
    """

    id: int
    ime: str
    cas_priprave: int
    postopek: str
    kratek_opis: str
    avtor_id: int
    avtor: str
    tezavnost_id: int
    tezavnost: str
    kategorija_id: int
    kategorija: str


@dataclass
class Sestavina:
    """Sestavina in njena običajna merska enota."""

    id: int
    ime: str
    enota: str

@dataclass
class Pripomocek:
    """Kuhinjski pripomoček, potreben za pripravo sladice."""

    id: int
    ime: str

@dataclass
class SestavinaRecepta:
    """Sestavina skupaj s količino, ki jo zahteva določen recept.

    ID, ime in enota pridejo iz tabele sestavina, količina pa iz
    povezovalne tabele vsebuje.
    """

    id: int
    ime: str
    kolicina: str
    enota: str
