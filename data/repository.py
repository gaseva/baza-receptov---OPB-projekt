from dataclasses import dataclass

import psycopg2

from . import auth_public as auth
from .models import oseba


@dataclass
class Sifrant:
    id: int
    ime: str


@dataclass
class SestavinaRecepta:
    id: int
    ime: str
    kolicina: str


@dataclass
class SladicaDTO:
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


class Repository:

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
            t.tezavnost,

            k.id AS kategorija_id,
            k.ime AS kategorija

        FROM sladica AS s
        JOIN oseba AS o
            ON o.id = s.avtor
        JOIN tezavnost AS t
            ON t.id = s.tezavnost
        JOIN kategorija AS k
            ON k.id = s.kategorija
    """

    def __init__(self):
        """Odpre povezavo s PostgreSQL bazo."""

        self.conn = psycopg2.connect(
            dbname=auth.db,
            host=auth.host,
            user=auth.user,
            password=auth.password,
            port=auth.port
        )

    def zapri(self):
        """Zapre povezavo z bazo."""

        if self.conn and not self.conn.closed:
            self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.zapri()

    # =========================================================
    # OSEBE
    # =========================================================

    def dobi_osebo(self, id: int) -> oseba | None:
        """Vrne osebo z izbranim ID-jem."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        ime,
                        priimek,
                        elektronski_naslov,
                        uporabnisko_ime,
                        geslo
                    FROM oseba
                    WHERE id = %s
                    """,
                    (id,)
                )

                vrstica = cur.fetchone()

        if vrstica is None:
            return None

        return oseba(*vrstica)

    def dobi_osebo_po_uporabniskem_imenu(
        self,
        uporabnisko_ime: str
    ) -> oseba | None:
        """Poišče osebo po uporabniškem imenu."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        ime,
                        priimek,
                        elektronski_naslov,
                        uporabnisko_ime,
                        geslo
                    FROM oseba
                    WHERE uporabnisko_ime = %s
                    """,
                    (uporabnisko_ime,)
                )

                vrstica = cur.fetchone()

        if vrstica is None:
            return None

        return oseba(*vrstica)

    def dobi_vse_osebe(self) -> list[oseba]:
        """Vrne seznam vseh oseb."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        id,
                        ime,
                        priimek,
                        elektronski_naslov,
                        uporabnisko_ime,
                        geslo
                    FROM oseba
                    ORDER BY priimek, ime
                    """
                )

                vrstice = cur.fetchall()

        return [oseba(*vrstica) for vrstica in vrstice]

    def dodaj_osebo(
        self,
        ime: str,
        priimek: str,
        elektronski_naslov: str,
        uporabnisko_ime: str,
        geslo_hash: str
    ) -> int:
        """
        Doda novo osebo in vrne njen ID.

        Parameter geslo_hash mora vsebovati že zgoščeno geslo,
        ne navadnega gesla.
        """

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO oseba (
                        ime,
                        priimek,
                        elektronski_naslov,
                        uporabnisko_ime,
                        geslo
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        ime,
                        priimek,
                        elektronski_naslov,
                        uporabnisko_ime,
                        geslo_hash
                    )
                )

                novi_id = cur.fetchone()[0]

        return novi_id

    # =========================================================
    # SLADICE
    # =========================================================

    @staticmethod
    def _ustvari_sladico_dto(vrstica) -> SladicaDTO:
        return SladicaDTO(*vrstica)

    def dobi_vse_sladice(self) -> list[SladicaDTO]:
        """Vrne vse sladice skupaj z avtorjem, težavnostjo in kategorijo."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    self.SQL_SLADICE + """
                    ORDER BY s.ime
                    """
                )

                vrstice = cur.fetchall()

        return [
            self._ustvari_sladico_dto(vrstica)
            for vrstica in vrstice
        ]

    def dobi_sladico(self, id: int) -> SladicaDTO | None:
        """Vrne posamezno sladico."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    self.SQL_SLADICE + """
                    WHERE s.id = %s
                    """,
                    (id,)
                )

                vrstica = cur.fetchone()

        if vrstica is None:
            return None

        return self._ustvari_sladico_dto(vrstica)

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
        pripomocki: list[int] | None = None
    ) -> int:
        """
        Doda sladico, njene sestavine in pripomočke.

        sestavine:
            seznam parov (id_sestavine, kolicina)

        Primer:
            [(1, "200 g"), (36, "3 kosi")]

        pripomocki:
            seznam ID-jev pripomočkov
        """

        sestavine = sestavine or []
        pripomocki = pripomocki or []

        # Vse poizvedbe se izvedejo v eni transakciji.
        with self.conn:
            with self.conn.cursor() as cur:

                cur.execute(
                    """
                    INSERT INTO sladica (
                        ime,
                        cas_priprave,
                        postopek,
                        kratek_opis,
                        avtor,
                        tezavnost,
                        kategorija
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        ime,
                        cas_priprave,
                        postopek,
                        kratek_opis,
                        avtor_id,
                        tezavnost_id,
                        kategorija_id
                    )
                )

                sladica_id = cur.fetchone()[0]

                for sestavina_id, kolicina in sestavine:
                    cur.execute(
                        """
                        INSERT INTO vsebuje (
                            sladica,
                            sestavina,
                            kolicina_sestavine
                        )
                        VALUES (%s, %s, %s)
                        ON CONFLICT (sladica, sestavina)
                        DO UPDATE SET
                            kolicina_sestavine =
                                EXCLUDED.kolicina_sestavine
                        """,
                        (
                            sladica_id,
                            sestavina_id,
                            kolicina
                        )
                    )

                for pripomocek_id in set(pripomocki):
                    cur.execute(
                        """
                        INSERT INTO potrebujes (
                            sladica,
                            pripomocek
                        )
                        VALUES (%s, %s)
                        ON CONFLICT (sladica, pripomocek)
                        DO NOTHING
                        """,
                        (
                            sladica_id,
                            pripomocek_id
                        )
                    )

        return sladica_id

    # =========================================================
    # KATEGORIJE IN TEŽAVNOSTI
    # =========================================================

    def dobi_kategorije(self) -> list[Sifrant]:
        """Vrne vse kategorije."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, ime
                    FROM kategorija
                    ORDER BY ime
                    """
                )

                vrstice = cur.fetchall()

        return [Sifrant(*vrstica) for vrstica in vrstice]

    def dobi_tezavnosti(self) -> list[Sifrant]:
        """Vrne vse stopnje težavnosti."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, tezavnost
                    FROM tezavnost
                    ORDER BY id
                    """
                )

                vrstice = cur.fetchall()

        return [Sifrant(*vrstica) for vrstica in vrstice]

    # =========================================================
    # SESTAVINE
    # =========================================================

    def dobi_vse_sestavine(self) -> list[Sifrant]:
        """Vrne vse sestavine."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, ime
                    FROM sestavina
                    ORDER BY ime
                    """
                )

                vrstice = cur.fetchall()

        return [Sifrant(*vrstica) for vrstica in vrstice]

    def dobi_sestavine_sladice(
        self,
        sladica_id: int
    ) -> list[SestavinaRecepta]:
        """Vrne sestavine in količine za izbrano sladico."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        s.id,
                        s.ime,
                        v.kolicina_sestavine
                    FROM vsebuje AS v
                    JOIN sestavina AS s
                        ON s.id = v.sestavina
                    WHERE v.sladica = %s
                    ORDER BY s.ime
                    """,
                    (sladica_id,)
                )

                vrstice = cur.fetchall()

        return [
            SestavinaRecepta(*vrstica)
            for vrstica in vrstice
        ]

    # =========================================================
    # PRIPOMOČKI
    # =========================================================

    def dobi_vse_pripomocke(self) -> list[Sifrant]:
        """Vrne vse pripomočke."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, ime
                    FROM pripomocek
                    ORDER BY ime
                    """
                )

                vrstice = cur.fetchall()

        return [Sifrant(*vrstica) for vrstica in vrstice]

    def dobi_pripomocke_sladice(
        self,
        sladica_id: int
    ) -> list[Sifrant]:
        """Vrne pripomočke za izbrano sladico."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT
                        p.id,
                        p.ime
                    FROM potrebujes AS po
                    JOIN pripomocek AS p
                        ON p.id = po.pripomocek
                    WHERE po.sladica = %s
                    ORDER BY p.ime
                    """,
                    (sladica_id,)
                )

                vrstice = cur.fetchall()

        return [Sifrant(*vrstica) for vrstica in vrstice]

    # =========================================================
    # PRILJUBLJENI RECEPTI
    # =========================================================

    def dodaj_med_priljubljene(
        self,
        oseba_id: int,
        sladica_id: int
    ) -> None:
        """Doda sladico med priljubljene recepte uporabnika."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO priljubljeno (
                        sladica,
                        oseba
                    )
                    VALUES (%s, %s)
                    ON CONFLICT (sladica, oseba)
                    DO NOTHING
                    """,
                    (
                        sladica_id,
                        oseba_id
                    )
                )

    def odstrani_iz_priljubljenih(
        self,
        oseba_id: int,
        sladica_id: int
    ) -> None:
        """Odstrani sladico iz priljubljenih receptov."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM priljubljeno
                    WHERE oseba = %s
                      AND sladica = %s
                    """,
                    (
                        oseba_id,
                        sladica_id
                    )
                )

    def dobi_priljubljene(
        self,
        oseba_id: int
    ) -> list[SladicaDTO]:
        """Vrne priljubljene sladice uporabnika."""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    self.SQL_SLADICE + """
                    JOIN priljubljeno AS p
                        ON p.sladica = s.id
                    WHERE p.oseba = %s
                    ORDER BY s.ime
                    """,
                    (oseba_id,)
                )

                vrstice = cur.fetchall()

        return [
            self._ustvari_sladico_dto(vrstica)
            for vrstica in vrstice
        ]