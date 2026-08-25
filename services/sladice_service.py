from data.repository import repo


class SladiceService:

    def __init__(self):
        self.repository = repo()

    def dobi_vse_sladice(self):
        return self.repository.dobi_vse_sladice()