from data.repository import Repository


class SladiceService:
    def dobi_vse_sladice(self):
        with Repository() as repository:
            return repository.dobi_vse_sladice()

    def dobi_recept(self, sladica_id):
        """
        Vrne sladico in vse sestavine, ki pripadajo tej sladici.
        """
        with Repository() as repository:
            sladica = repository.dobi_sladico(sladica_id)

            if sladica is None:
                return None, []

            sestavine = repository.dobi_sestavine_za_sladico(sladica_id)

            return sladica, sestavine

    
    def poisci_sladice(self, iskanje, kategorija_id=None):
        """Išče po imenu/sladici in po neobvezni kategoriji."""

        iskanje = (iskanje or "").strip()

        kategorija_id = (
            ""
            if kategorija_id is None
            else str(kategorija_id).strip()
        )

        if kategorija_id:
            try:
                kategorija_id = int(kategorija_id)
            except ValueError:
                return []
        else:
            kategorija_id = None

        with Repository() as repository:
            if not iskanje and kategorija_id is None:
                return repository.dobi_vse_sladice()

            return repository.poisci_sladice(
                iskanje,
                kategorija_id,
            )

    def dobi_kategorije(self):
        """Vrne kategorije za dropdown na domači strani."""
    
        with Repository() as repository:
            return repository.dobi_kategorije()

    def dodaj_sladico(
            self,
            ime,
            cas_priprave,
            postopek,
            kratek_opis,
            avtor_id,
            tezavnost_id,
            kategorija_id,
            sestavina_ids,
            kolicine,
            pripomocek_ids,
        ):
            """Preveri podatke obrazca in doda celoten recept v bazo."""

            ime = (ime or "").strip() # odstranjevanje odvečnih presledkov
            cas_priprave = (cas_priprave or "").strip()
            postopek = (postopek or "").strip()
            kratek_opis = (kratek_opis or "").strip()

            if not ime:
                raise ValueError("Vnesti moraš ime sladice.") # preverjanje obveznih podatkov
            if not cas_priprave:
                raise ValueError("Vnesti moraš čas priprave.")
            if not postopek:
                raise ValueError("Vnesti moraš postopek priprave.")
            if not kratek_opis:
                raise ValueError("Vnesti moraš kratek opis.")

            try:
                ure, minute = map(int, cas_priprave.split(":")) # pretvorba časa v minute
                cas_priprave_minute = ure * 60 + minute
            except (TypeError, ValueError):
                raise ValueError("Čas priprave ni v pravilni obliki.")

            if cas_priprave_minute <= 0:
                raise ValueError("Čas priprave mora biti daljši od 0 minut.")


            # to pomojem lahko zbriševa
            try:
                avtor_id = int(avtor_id)
                tezavnost_id = int(tezavnost_id)
                kategorija_id = int(kategorija_id)
            except (TypeError, ValueError):
                raise ValueError("Izberi veljavno težavnost in kategorijo.")

            sestavina_ids = sestavina_ids or []
            kolicine = kolicine or []

            if len(sestavina_ids) != len(kolicine):
                raise ValueError("Podatki o sestavinah niso popolni.")

            sestavine = []

            for sestavina_id, kolicina in zip(sestavina_ids, kolicine):
                sestavina_id = (sestavina_id or "").strip()
                kolicina = (kolicina or "").strip()

                # popolnoma prazno dodatno vrstico preskočimo
                if not sestavina_id and not kolicina:
                    continue

                if not sestavina_id or not kolicina:
                    raise ValueError(
                        "Pri vsaki sestavini izberi sestavino in vnesi količino."
                    )

                try:
                    sestavina_id = int(sestavina_id)
                    kolicina_stevilo = int(kolicina)
                except ValueError:
                    raise ValueError("Količina sestavine mora biti celo število.")

                if kolicina_stevilo <= 0:
                    raise ValueError("Količina sestavine mora biti večja od 0.")

                sestavine.append((sestavina_id, str(kolicina_stevilo)))

            if not sestavine:
                raise ValueError("Recept mora vsebovati vsaj eno sestavino.")

            try:
                pripomocki = [
                    int(pripomocek_id)
                    for pripomocek_id in (pripomocek_ids or [])
                    if (pripomocek_id or "").strip()
                ]
            except ValueError:
                raise ValueError("Izbran pripomoček ni veljaven.")

            with Repository() as repository:
                return repository.dodaj_sladico(
                    ime=ime,
                    cas_priprave=cas_priprave_minute,
                    postopek=postopek,
                    kratek_opis=kratek_opis,
                    avtor_id=avtor_id,
                    tezavnost_id=tezavnost_id,
                    kategorija_id=kategorija_id,
                    sestavine=sestavine,
                    pripomocki=pripomocki,
                )


    def dobi_vse_sestavine(self):
        """Vrne vse sestavine za prikaz v dropdownu."""

        with Repository() as repository:
            return repository.dobi_vse_sestavine()


    def dodaj_sestavino(self, ime: str, enota: str):
        """Preveri podatke in doda novo sestavino."""

        ime = (ime or "").strip() # odstrani pressledke na začetku in na koncu
        enota = (enota or "").strip()

        if not ime:
            raise ValueError("Vnesti moraš ime sestavine.") #preprečitev praznega imena

        if not enota:
            raise ValueError("Vnesti moraš mersko enoto.")

        with Repository() as repository:
            obstojeca_sestavina = repository.dobi_sestavino_po_imenu(ime)

            if obstojeca_sestavina is not None: # preverimo ali sestavina že obstaja
                raise ValueError(
                    f"Sestavina »{obstojeca_sestavina.ime}« že obstaja."
                )

            return repository.dodaj_sestavino(ime, enota) # dodamo sestavino in enoto v bazo preko repozitorija


    def dobi_vse_pripomocke(self):
        """Vrne vse pripomočke za prikaz v dropdownu."""

        with Repository() as repository:
            return repository.dobi_vse_pripomocke()

    def dodaj_pripomocek(self, ime: str):
        """Preveri podatke in doda nov pripomoček."""

        ime = (ime or "").strip()

        if not ime:
            raise ValueError("Vnesti moraš ime pripomočka.")

        with Repository() as repository:
            obstojeci_pripomocek = repository.dobi_pripomocek_po_imenu(ime)

            if obstojeci_pripomocek is not None:
                raise ValueError(
                    f"Pripomoček »{obstojeci_pripomocek.ime}« že obstaja."
                )

            return repository.dodaj_pripomocek(ime)
        
    def dobi_najbolj_priljubljene_sladice(
        self,
        omejitev: int = 10
    ):
        if omejitev < 1:
            return []

        with Repository() as repository:
            return repository.dobi_najbolj_priljubljene_sladice(
                omejitev
            )