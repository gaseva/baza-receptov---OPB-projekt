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