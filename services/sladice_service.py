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