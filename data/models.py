# tukaj bova vpisali classe
from dataclasses import dataclass
from datetime import datetime

@dataclass
class oseba:
    id: int
    ime: str
    priimek: str
    elektronski_naslov: str
    uporabnisko_ime: str
    geslo: str

@dataclass
class sladica:
    id: int
    ime: str
    cas_priprave: int
    postopek: str
    kratek_opis: str

@dataclass
class tezavnost:
    id: int
    tezavnost: str


@dataclass
class kategorija:
    id: int
    ime: str


@dataclass
class sestavina:
    id: int
    ime: str



@dataclass
class pripomocek:
    id: int
    ime: str
