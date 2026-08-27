
# tukaj so podatkovni razredi, ki predstavljajo obliko podatkov
# en dataclass predstavlja eno entiteto
# ne povezuje se direktno z bazo, to dela repository

from dataclasses import dataclass


@dataclass
class Oseba:
    id: int
    ime: str
    priimek: str
    elektronski_naslov: str
    uporabnisko_ime: str
    geslo_hash: str
    rola: str

@dataclass
class Tezavnost:
    id: int
    tezavnost: str
    
    
@dataclass
class Kategorija:
    id: int
    ime: str


@dataclass
class Sladica:
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
    id: int
    ime: str
    enota: str

@dataclass
class Pripomocek:
    id: int
    ime: str

@dataclass
class SestavinaRecepta:
    id: int
    ime: str
    kolicina: str
    enota: str