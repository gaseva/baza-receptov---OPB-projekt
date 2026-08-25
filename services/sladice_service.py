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

    
    def poisci_sladice(self, iskanje):
        """Vrne sladice, katerih ime vsebuje iskalni niz."""
        with Repository() as repository:
            sladice = repository.dobi_vse_sladice()

        iskanje = (iskanje or "").strip().casefold()

        if not iskanje:
            return sladice

        return [
            sladica
            for sladica in sladice
            if iskanje in sladica.ime.casefold()
        ]


    def dobi_vse_sestavine(self):
        """Vrne vse sestavine za prikaz v dropdownu."""

        with Repository() as repository:
            return repository.dobi_vse_sestavine()


    def dodaj_sestavino(self, ime: str, enota: str):
        """Preveri podatke in doda novo sestavino."""
    
        ime = (ime or "").strip()
        enota = (enota or "").strip()
    
        if not ime:
            raise ValueError("Vnesti moraš ime sestavine.")
    
        if not enota:
            raise ValueError("Vnesti moraš mersko enoto.")
    
        with Repository() as repository:
            obstojeca_sestavina = repository.dobi_sestavino_po_imenu(ime)
    
            if obstojeca_sestavina is not None:
                raise ValueError(
                    f"Sestavina »{obstojeca_sestavina.ime}« že obstaja."
                )
    
            return repository.dodaj_sestavino(ime, enota)