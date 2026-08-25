from data.repository import Repository as repo


class SladiceService:
    def __init__(self):
        self.repository = repo()

    def dobi_vse_sladice(self):
        return self.repository.dobi_vse_sladice()



    def dobi_recept(self, sladica_id):
        '''
        Vrne sladico in vse sestavine, ki pripadajo tej sladici.
        '''
        sladica = self.repository.dobi_sladico(sladica_id)

        if sladica is None:
            return None, []

        sestavine = self.repository.dobi_sestavine_za_sladico(sladica_id)
        return sladica, sestavine


#    def poisci_sladice(self, iskanje):
#        """Vrne sladice, ki se ujemajo z iskalnim nizom."""
#        sladice = self.repository.dobi_vse_sladice()
#        iskanje = (iskanje or "").strip().casefold()
#
#        if not iskanje:
#            return sladice
#
#        return [
#            sladica
#            for sladica in sladice
#            if iskanje in sladica.ime.casefold()
#            or iskanje in (sladica.kratek_opis or "").casefold()
#            or iskanje in (sladica.kategorija or "").casefold()
#        ]