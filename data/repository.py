# vmesnik med aplikacijo in bazo
# izvaja SQL poizvedbe
# rezultate pretvarja v podatkovne razrede

import psycopg2 # psycopg2 povezuje python s postgresql
from . import auth_public as auth
from .models import (
    Kategorija,
    Oseba,
    Pripomocek,
    Sestavina,
    SestavinaRecepta,
    Sladica,
    Tezavnost
)


class Repository:
    # v tem razredu so zdruzene vse funkcije za delo z bazo

    # pridobivanje vseh podatkov o sladicah
    # sva naredili da sql kode ni treba ponavljat
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
    # self predstavlja trenutni objekt razreda repository


    # ustvari povezavo z bazo in jo shrani v self.conn
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=auth.db,
            host=auth.host,
            user=auth.user,
            password=auth.password,
            port=auth.port
        )




    # v repository vrne trenutni objekt
    def __enter__(self):
        return self




    # ob koncu bloka wwith zapre povezavo z bazo
    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()




    #######
    # OSEBE 
    #######

    def dobi_osebo_po_uporabniskem_imenu(self, uporabnisko_ime: str) -> Oseba | None:
        """poišče osebo z določenim uporabniškim imenom"""
        # uporablja se pri prijavi in preverjanju zasedenosti uporabniškega imena

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, ime, priimek, elektronski_naslov,
                           uporabnisko_ime, geslo_hash, rola
                    FROM oseba
                    WHERE uporabnisko_ime = %s
                    """,
                    (uporabnisko_ime,)
                )
                vrstica = cur.fetchone()

        return None if vrstica is None else Oseba(*vrstica)

    


    def dobi_osebo_po_elektronskem_naslovu(self, elektronski_naslov: str) -> Oseba | None:
        """poišče osebo z določenim elektronskim naslovom"""
        # uporablja se pri registraciji za enoličnost elektronskega naslova

        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, ime, priimek, elektronski_naslov,
                        uporabnisko_ime, geslo_hash, rola
                FROM oseba
                WHERE elektronski_naslov = %s
                """,
                (elektronski_naslov,)
            )

            vrstica = cur.fetchone()

        return None if vrstica is None else Oseba(*vrstica)




    def dodaj_osebo(
        self,
        ime: str,
        priimek: str,
        elektronski_naslov: str,
        uporabnisko_ime: str,
        geslo_hash: str
    )-> int:
        """doda osebo v bazo """

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO oseba (
                        ime, priimek, elektronski_naslov,
                        uporabnisko_ime, geslo_hash
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        ime,
                        priimek,
                        elektronski_naslov,
                        uporabnisko_ime,
                        geslo_hash,
                    ),
                )
                
                oseba_id = cur.fetchone()[0]

        return oseba_id




    #########
    # SLADICE 
    #########
    
    @staticmethod
    def _ustvari_sladico(vrstica) -> Sladica:
        """pretvori sql vrstico v objekt sladica"""

        return Sladica(*vrstica)


    

    def dobi_vse_sladice(self) -> list[Sladica]:
        """vrne vse sladice"""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(self.SQL_SLADICE + " ORDER BY s.ime")
                vrstice = cur.fetchall()

        return [self._ustvari_sladico(vrstica) for vrstica in vrstice]




    def poisci_sladice(self, iskanje: str, kategorija_id: int | None = None) -> list[Sladica]:
        """išče po imenu sladice in/ali po kategoriji"""
        # ILIKE ne razlikuje med malimi in velikimi črkami

        vzorec = f"%{iskanje}%"

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    self.SQL_SLADICE
                    + """
                    WHERE (
                        %s = ''
                        OR s.ime ILIKE %s 
                        OR EXISTS (
                            SELECT 1
                            FROM vsebuje AS v
                            JOIN sestavina AS se
                                ON se.id = v.sestavina
                            WHERE v.sladica = s.id
                                AND se.ime ILIKE %s
                        )
                    )
                    AND (%s IS NULL OR s.kategorija = %s)
                    ORDER BY s.ime
                    """,
                    (
                        iskanje,
                        vzorec,
                        vzorec,
                        kategorija_id,
                        kategorija_id
                    ),
                )
                vrstice = cur.fetchall()

        return [
            self._ustvari_sladico(vrstica)
            for vrstica in vrstice
        ]




    def dobi_sladico(self, sladica_id: int) -> Sladica | None:
        """pridobi sladico glede na njen ID"""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    self.SQL_SLADICE + " WHERE s.id = %s",
                    (sladica_id,)
                )
                vrstica = cur.fetchone()

        return None if vrstica is None else self._ustvari_sladico(vrstica)




    # funkcija doda sladico v bazo
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
    

        sestavine = sestavine or []
        pripomocki = pripomocki or []

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO sladica (
                        ime, cas_priprave, postopek, kratek_opis,
                        avtor, tezavnost, kategorija
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
                    ),
                )
                sladica_id = cur.fetchone()[0]

                # vsebuje povezuje sladico s sestavinami in količinami
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

                # odstranitev podvojenih pripomočkov
                for pripomocek_id in set(pripomocki):
                    cur.execute(
                        """
                        INSERT INTO potrebujes (sladica, pripomocek)
                        VALUES (%s, %s)
                        ON CONFLICT (sladica, pripomocek) DO NOTHING
                        """,
                        (sladica_id, pripomocek_id)
                    )

        return sladica_id




    def dobi_sestavine_za_sladico(
        self, sladica_id: int
    ) -> list[SestavinaRecepta]:
        """vrne imena in koičine sestavin za izbrano sladico"""
        # povezuje tabelo vsebuje z količino in sestavina z imenom in enoto

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
                    (sladica_id,)
                )
                vrstice = cur.fetchall()

        return [SestavinaRecepta(*vrstica) for vrstica in vrstice]
    


    
    def dobi_najbolj_priljubljene_sladice(
        self,
        omejitev: int = 10
    ) -> list[Sladica]:
        """
        vrne tiste sladice, ki jih je največ uporabnikov označilo kot priljubljene
        """

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    self.SQL_SLADICE
                    + """
                    JOIN priljubljeno AS p
                        ON p.sladica = s.id

                    GROUP BY
                        s.id,
                        s.ime,
                        s.cas_priprave,
                        s.postopek,
                        s.kratek_opis,
                        o.id,
                        o.ime,
                        o.priimek,
                        t.id,
                        t.ime,
                        k.id,
                        k.ime

                    ORDER BY
                        COUNT(p.oseba) DESC,
                        s.ime

                    LIMIT %s
                    """,
                    (omejitev,)
                )

                vrstice = cur.fetchall()

                return [
                    self._ustvari_sladico(vrstica)
                    for vrstica in vrstice
                ]




    ###########################################################
    # ŠIFRANTI: KATEGORIJE, TEŽAVNOSTI, SESTAVINE IN PRIPOMOČKI
    ###########################################################

    def dobi_kategorije(self) -> list[Kategorija]:
        """Vvrne vse kategorije kot seznam objektov Kategorija"""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, ime FROM kategorija ORDER BY ime")
                vrstice = cur.fetchall()

        return [Kategorija(*vrstica) for vrstica in vrstice]




    def dobi_vse_sestavine(self) -> list[Sestavina]:
        """vrne ID, ime in enoto vseh sestavin"""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, ime, enota FROM sestavina ORDER BY ime")
                vrstice = cur.fetchall()

        return [Sestavina(*vrstica) for vrstica in vrstice]




    def dobi_sestavino_po_imenu(self, ime: str) -> Sestavina | None:
        """poišče sestavino po imenu"""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, ime, enota
                    FROM sestavina
                    WHERE LOWER(ime) = LOWER(%s)
                    """,
                    (ime,)
                )

                vrstica = cur.fetchone()

        return None if vrstica is None else Sestavina(*vrstica)




    def dodaj_sestavino(self, ime: str, enota: str) -> Sestavina:
        """doda novo sestavino v bazo in vrne objekt Sestavina"""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO sestavina (ime, enota)
                    VALUES (%s, %s)
                    RETURNING id, ime, enota
                    """,
                    (ime, enota)
                )

                vrstica = cur.fetchone()

        return Sestavina(*vrstica)




    def dobi_vse_pripomocke(self) -> list[Pripomocek]:
        """vrne vse pripomočke za prikaz v dropdownu"""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, ime FROM pripomocek ORDER BY ime")
                vrstice = cur.fetchall()

        return [Pripomocek(*vrstica) for vrstica in vrstice]




    def dobi_pripomocek_po_imenu(self, ime: str) -> Pripomocek | None:
        """poišče pripomoček po imenu"""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, ime
                    FROM pripomocek
                    WHERE LOWER(ime) = LOWER(%s)
                    """,
                    (ime,)
                )
                vrstica = cur.fetchone()

        return None if vrstica is None else Pripomocek(*vrstica)




    def dodaj_pripomocek(self, ime: str) -> Pripomocek:
        """doda nov pripomoček v bazo in vrne objekt Pripomocek"""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO pripomocek (ime)
                    VALUES (%s)
                    RETURNING id, ime
                    """,
                    (ime,)
                )
                vrstica = cur.fetchone()

        return Pripomocek(*vrstica)
    



    def dobi_pripomocke_sladice(self, sladica_id: int) -> list[Pripomocek]:
        """pridobi pripomočke za določen recept"""

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
                    (sladica_id,)
                )
                vrstice = cur.fetchall()

        return [Pripomocek(*vrstica) for vrstica in vrstice]




    ##############################
    # PRILJUBLJENE IN MOJE SLADICE
    ##############################

    def dodaj_med_priljubljene(self, oseba_id: int, sladica_id: int) -> None:
        """v tabelo priljubljeno doda povezavo med osebo in sladico"""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO priljubljeno (sladica, oseba)
                    VALUES (%s, %s)
                    ON CONFLICT (sladica, oseba) DO NOTHING
                    """,
                    (sladica_id, oseba_id)
                )




    def odstrani_iz_priljubljenih(
        self, oseba_id: int, sladica_id: int
    ) -> None:
        """odstrani povezavo oseba-sladica"""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    DELETE FROM priljubljeno
                    WHERE oseba = %s AND sladica = %s
                    """,
                    (oseba_id, sladica_id)
                )




    def je_priljubljena(self, oseba_id: int, sladica_id: int) -> bool:
        """pove ali je recept priljubljen določeni osebi"""

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
                    (oseba_id, sladica_id)
                )
                return cur.fetchone()[0]




    def dobi_priljubljene_recepte(self, oseba_id: int) -> list[Sladica]:
        """vrne vse priljubljene sladice izbranega uporabnika"""

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    self.SQL_SLADICE
                    + """
                    JOIN priljubljeno AS p ON p.sladica = s.id
                    WHERE p.oseba = %s
                    ORDER BY s.ime
                    """,
                    (oseba_id,)
                )
                vrstice = cur.fetchall()

        return [self._ustvari_sladico(vrstica) for vrstica in vrstice]




    def dobi_id_priljubljenih_receptov(self, oseba_id: int) -> set[int]:
        """vrne ID priljubljenih sladic izbranega uporabnika"""
        # na tej podlagi HTML pokaže poln/prazen srček

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT sladica
                    FROM priljubljeno
                    WHERE oseba = %s
                    """,
                    (oseba_id,)
                )

                return {vrstica[0] for vrstica in cur.fetchall()}




    def dobi_sladice_avtorja(
        self,
        oseba_id: int
    ) -> list[Sladica]:
        """
        vrne vse sladice, ki jih je dodal določen uporabnik
        """

        with self.conn:
            with self.conn.cursor() as cur:
                cur.execute(
                    self.SQL_SLADICE
                    + """
                    WHERE s.avtor = %s
                    ORDER BY s.ime
                    """,
                    (oseba_id,)
                )

                vrstice = cur.fetchall()

                return [
                    self._ustvari_sladico(vrstica)
                    for vrstica in vrstice
                ]