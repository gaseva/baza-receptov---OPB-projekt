# tukaj bova vpisali classe
from dataclasses import dataclass
from datetime import datetime
## import bcrypt 
import csv
from psycopg import connect, sql 
## from psycopg.errors import IntegrityError 
## from auth import auth


@dataclass
class oseba:
    id: int
    ime: str
    priimek: str
    elektronski_naslov: str
    uporabnisko_ime: str
    geslo: str


    @classmethod
    def uvozi_podatke(cls):
        with conn.transaction():
            with conn.cursor() as cur:
                with open('podatki.csv') as f:
                    rd = csv.reader(f)
                    stolpci = next(rd)
                    for vrstica in rd:
                        podatki = dict(zip(stolpci, vrstica))
                        #if podatki['geslo']:
                        #    podatki['geslo'] = Oseba._nastavi_geslo(podatki['geslo'])
                        #else:
                        #    podatki['geslo'] = None
                        cur.execute(
                            """
                            INSERT INTO oseba (id, ime, priimek, elektronski_naslov, uporabnisko_ime, geslo))
                            VALUES (%(id)s, %(ime)s, %(priimek)s, %(elektronski_naslov)s, %(uporabnisko_ime)s, %(geslo)s)

                            
                            """, podatki
                        )

@dataclass
class sladica:
    id: int
    ime: str
    cas_priprave: int
    postopek: str
    kratek_opis: str

    @classmethod
    def uvozi_podatke(cls):
        with conn.transaction():
            with conn.cursor() as cur:
                with open('podatki.csv') as f:
                    rd = csv.reader(f)
                    stolpci = next(rd)
                    for vrstica in rd:
                        podatki = dict(zip(stolpci, vrstica))
                        cur.execute(
                            """
                            INSERT INTO sladica (id, ime, cas_priprave, postopek, kratek_opis, avtor, tezavnost, kategorija)
                            VALUES (%(id)s, %(ime)s, %(cas_priprave)s, %(postopek)s, %(kratek_opis)s, %(avtor)s, %(tezavnost)s, %(kategorija)s)

                            %to še je treba popravit in prilagodit glede na najin csv
                            """, podatki
                        )

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
