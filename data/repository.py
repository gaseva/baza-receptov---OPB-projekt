"""Dostop do podatkov v PostgreSQL bazi."""

import psycopg2
import psycopg2.extras

from . import auth_public as auth

from .models import (
    Kategorija,
    Oseba,
    Pripomocek,
    Sestavina,
    SestavinaRecepta,
    Sladica,
    Tezavnost,
)


class Repository:
    """Vse poizvedbe za dostop do baze.

    Primer uporabe::

        with Repository() as repo:
            sladice = repo.dobi_vse_sladice()

    Ko se blok with konča, se povezava samodejno zapre.
    """

    # Osnovni SELECT za pridobivanje vseh podatkov o sladicah
    SQL_SLADICE = """
        SELECT
            s.id,
            s.ime,
            s.cas_priprave,
            s.postopek,
            s.kratek_opis,
            o.id AS avtor_id,
            o.ime || ' ' || o.priimek AS avtor,
            t.id AS tezavnost_id,
            t.ime,
            k.id AS kategorija_id,
            k.ime AS kategorija
        FROM sladica AS s
        JOIN oseba AS o ON o.id = s.avtor
        JOIN tezavnost AS t ON t.id = s.tezavnost
        JOIN kategorija AS k ON k.id = s.kategorija
    """

    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=auth.db,
            host=auth.host,
            user=auth.user,
            password=auth.password,
            port=auth.port,
        )

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

    # =====================================================================
    # OSEBE
    # =====================================================================

    def dobi_osebo(self, oseba_id: int) -> Oseba | None:
        """Vrne osebo z danim ID-jem ali None, če oseba ne obstaja."""

        # with self.conn predstavlja transakcijo. Ob uspehu se izvede COMMIT,
        # ob napaki pa ROLLBACK. Cursor se po notranjem bloku sam zapre.
        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, ime, priimek, elektronski_naslov,
                           uporabnisko_ime, geslo_hash, rola
                    FROM oseba
                    WHERE id = %s
                    """,
                    (oseba_id,),
                )
                vrstica = cur.fetchone()

        if vrstica is None:
            return None

        # Zvezdica razpakira šest vrednosti v konstruktor razreda Oseba.
        return Oseba(*vrstica)

    def dobi_osebo_po_uporabniskem_imenu(self, uporabnisko_ime: str) -> Oseba | None:
        """Poišče osebo po uporabniškem imenu (za prijavo)"""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, ime, priimek, elektronski_naslov,
                           uporabnisko_ime, geslo_hash, rola
                    FROM oseba
                    WHERE uporabnisko_ime = %s
                    """,
                    (uporabnisko_ime,),
                )
                vrstica = cur.fetchone()

        return None if vrstica is None else Oseba(*vrstica)

# to nevem če zares rabima
    def dobi_vse_osebe(self) -> list[Oseba]:
        """Vrne vse osebe, urejene po priimku in imenu."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, ime, priimek, elektronski_naslov,
                           uporabnisko_ime, geslo_hash, rola
                    FROM oseba
                    ORDER BY priimek, ime
                    """
                )
                vrstice = cur.fetchall()

        return [Oseba(*vrstica) for vrstica in vrstice]

    def dodaj_osebo(
        self,
        ime: str,
        priimek: str,
        elektronski_naslov: str,
        uporabnisko_ime: str,
        geslo_hash: str,
    )-> None:
        """Doda osebo v bazo """

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO oseba (
                        ime, priimek, elektronski_naslov,
                        uporabnisko_ime, geslo_hash
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        ime,
                        priimek,
                        elektronski_naslov,
                        uporabnisko_ime,
                        geslo_hash,
                    ),
                )


    # =====================================================================
    # SLADICE
    # =====================================================================

    @staticmethod
    def _ustvari_sladico(vrstica) -> Sladica:
        """Pretvori eno SQL-vrstico v objekt Sladica iz models.py."""

        return Sladica(*vrstica)

    def dobi_vse_sladice(self) -> list[Sladica]:
        """Vrne vse sladice z avtorjem, težavnostjo in kategorijo."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(self.SQL_SLADICE + " ORDER BY s.ime")
                vrstice = cur.fetchall()

        return [self._ustvari_sladico(vrstica) for vrstica in vrstice]

    def dobi_sladico(self, sladica_id: int) -> Sladica | None:
        """Vrne eno sladico ali None, če tak ID ne obstaja."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    self.SQL_SLADICE + " WHERE s.id = %s",
                    (sladica_id,),
                )
                vrstica = cur.fetchone()

        return None if vrstica is None else self._ustvari_sladico(vrstica)

    def dodaj_sladico(
        self,
        ime: str,
        cas_priprave: int,
        postopek: str,
        kratek_opis: str,
        avtor_id: int,
        tezavnost_id: int,
        kategorija_id: int,
        sestavine: list[tuple[int, str]] | None = None,
        pripomocki: list[int] | None = None,
    ) -> int:
        """Doda sladico, sestavine in pripomočke v eni transakciji.

        sestavine so pari (id_sestavine, kolicina), na primer
        [(1, "200"), (3, "2")]. Enote tu ne podamo, saj je že shranjena v
        tabeli sestavina. Pripomocki so seznam ID-jev. Če pade vstavljanje
        ene povezave, se razveljavi tudi vstavljeni recept.
        """

        sestavine = sestavine or []
        pripomocki = pripomocki or []

        with self.conn:
            with self.conn.cursor() as cur:
                sladica_id = self._naslednji_id(cur, "sladica")
                cur.execute(
                    """
                    INSERT INTO sladica (
                        id, ime, cas_priprave, postopek, kratek_opis,
                        avtor, tezavnost, kategorija
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        sladica_id,
                        ime,
                        cas_priprave,
                        postopek,
                        kratek_opis,
                        avtor_id,
                        tezavnost_id,
                        kategorija_id,
                    ),
                )

                # vsebuje je povezovalna tabela med sladicami in sestavinami.
                for sestavina_id, kolicina in sestavine:
                    cur.execute(
                        """
                        INSERT INTO vsebuje (
                            sladica, sestavina, kolicina_sestavine
                        )
                        VALUES (%s, %s, %s)
                        ON CONFLICT (sladica, sestavina)
                        DO UPDATE SET
                            kolicina_sestavine = EXCLUDED.kolicina_sestavine
                        """,
                        (sladica_id, sestavina_id, kolicina),
                    )

                # set odstrani morebitne podvojene ID-je pripomočkov.
                for pripomocek_id in set(pripomocki):
                    cur.execute(
                        """
                        INSERT INTO potrebujes (sladica, pripomocek)
                        VALUES (%s, %s)
                        ON CONFLICT (sladica, pripomocek) DO NOTHING
                        """,
                        (sladica_id, pripomocek_id),
                    )

        return sladica_id

    def dobi_sestavine_za_sladico(
        self, sladica_id: int
    ) -> list[SestavinaRecepta]:
        """Vrne imena, količine in enote sestavin izbranega recepta."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT se.id, se.ime, v.kolicina_sestavine, se.enota
                    FROM vsebuje AS v
                    JOIN sestavina AS se ON se.id = v.sestavina
                    WHERE v.sladica = %s
                    ORDER BY se.ime
                    """,
                    (sladica_id,),
                )
                vrstice = cur.fetchall()

        return [SestavinaRecepta(*vrstica) for vrstica in vrstice]

    # =====================================================================
    # ŠIFRANTI: KATEGORIJE, TEŽAVNOSTI, SESTAVINE IN PRIPOMOČKI
    # =====================================================================

    def dobi_kategorije(self) -> list[Kategorija]:
        """Vrne vse kategorije, urejene po imenu."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, ime FROM kategorija ORDER BY ime")
                vrstice = cur.fetchall()

        return [Kategorija(*vrstica) for vrstica in vrstice]

    def dobi_tezavnosti(self) -> list[Tezavnost]:
        """Vrne težavnosti; besedilo stolpca tezavnost postane ime."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, ime FROM tezavnost ORDER BY id")
                vrstice = cur.fetchall()

        return [Tezavnost(*vrstica) for vrstica in vrstice]

    def dobi_vse_sestavine(self) -> list[Sestavina]:
        """Vrne ID, ime in enoto vseh sestavin, urejenih po imenu."""

        with self.conn:
            with self.conn.cursor() as cur:
                # Enota je del tabele sestavina, ne povezovalne tabele
                # vsebuje, zato jo izberemo neposredno od tukaj.
                cur.execute("SELECT id, ime, enota FROM sestavina ORDER BY ime")
                vrstice = cur.fetchall()

        return [Sestavina(*vrstica) for vrstica in vrstice]

    def dobi_sestavino_po_imenu(self, ime: str) -> Sestavina | None:
        """Vrne sestavino z danim imenom ali None, če ne obstaja."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, ime, enota
                    FROM sestavina
                    WHERE LOWER(ime) = LOWER(%s)
                    """,
                    (ime,),
                )

                # fetchone mora biti znotraj bloka za cursor
                vrstica = cur.fetchone()

        return None if vrstica is None else Sestavina(*vrstica)

    
    def dodaj_sestavino(self, ime: str, enota: str) -> Sestavina:
        """Doda novo sestavino in vrne ustvarjeni objekt."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO sestavina (ime, enota)
                    VALUES (%s, %s)
                    RETURNING id, ime, enota
                    """,
                    (ime, enota),
                )

                # Tudi tukaj mora biti fetchone znotraj bloka
                vrstica = cur.fetchone()

        return Sestavina(*vrstica)

    
    def dobi_sestavine_sladice(
        self, sladica_id: int
    ) -> list[SestavinaRecepta]:
        """Vrne imena, količine in enote sestavin izbranega recepta."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT se.id, se.ime, v.kolicina_sestavine, se.enota
                    FROM vsebuje AS v
                    JOIN sestavina AS se ON se.id = v.sestavina
                    WHERE v.sladica = %s
                    ORDER BY se.ime
                    """,
                    (sladica_id,),
                )
                vrstice = cur.fetchall()

        return [SestavinaRecepta(*vrstica) for vrstica in vrstice]

    def dobi_vse_pripomocke(self) -> list[Pripomocek]:
        """Vrne vse pripomočke, urejene po imenu."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, ime FROM pripomocek ORDER BY ime")
                vrstice = cur.fetchall()

        return [Pripomocek(*vrstica) for vrstica in vrstice]

    def dobi_pripomocke_sladice(self, sladica_id: int) -> list[Pripomocek]:
        """Vrne pripomočke, povezane z izbrano sladico."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT p.id, p.ime
                    FROM potrebujes AS po
                    JOIN pripomocek AS p ON p.id = po.pripomocek
                    WHERE po.sladica = %s
                    ORDER BY p.ime
                    """,
                    (sladica_id,),
                )
                vrstice = cur.fetchall()

        return [Pripomocek(*vrstica) for vrstica in vrstice]

    # =====================================================================
    # PRILJUBLJENE SLADICE
    # =====================================================================

    def dodaj_med_priljubljene(self, oseba_id: int, sladica_id: int) -> None:
        """Doda povezavo oseba-sladica, če še ne obstaja."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO priljubljeno (sladica, oseba)
                    VALUES (%s, %s)
                    ON CONFLICT (sladica, oseba) DO NOTHING
                    """,
                    (sladica_id, oseba_id),
                )

    def odstrani_iz_priljubljenih(
        self, oseba_id: int, sladica_id: int
    ) -> None:
        """Odstrani povezavo; ne izbriše niti osebe niti recepta."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM priljubljeno
                    WHERE oseba = %s AND sladica = %s
                    """,
                    (oseba_id, sladica_id),
                )

    def je_priljubljena(self, oseba_id: int, sladica_id: int) -> bool:
        """Pove, ali ima oseba izbrano sladico med priljubljenimi."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT EXISTS (
                        SELECT 1
                        FROM priljubljeno
                        WHERE oseba = %s AND sladica = %s
                    )
                    """,
                    (oseba_id, sladica_id),
                )
                return cur.fetchone()[0]

    def dobi_priljubljene(self, oseba_id: int) -> list[Sladica]:
        """Vrne vse priljubljene sladice izbrane osebe."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    self.SQL_SLADICE
                    + """
                    JOIN priljubljeno AS p ON p.sladica = s.id
                    WHERE p.oseba = %s
                    ORDER BY s.ime
                    """,
                    (oseba_id,),
                )
                vrstice = cur.fetchall()

        return [self._ustvari_sladico(vrstica) for vrstica in vrstice]
