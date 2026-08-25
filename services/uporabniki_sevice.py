from data.repository import Repository
import bcrypt
from datetime import date


class UporabnikiService:
    
    def dobi_vse_sladice(self):
        with Repository() as repository:
            return repository.dobi_vse_sladice()
        

    def registracija(self, ime: str, priimek: str, elektronski_naslov: str, uporabnisko_ime: str, geslo_hash: str, role: str):
        #zakodiramo geslo
        bytes = geslo_hash.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(bytes, salt)

        # Sedaj ustvarimo objekt Uporabnik in ga zapišemo bazo
        with Repository() as repository:
            o = Oseba(
                ime=ime,
                priimek=priimek,
                elektronski_naslov=elektronski_naslov,
                uporabnisko_ime=uporabnisko_ime,
                geslo_hash=password_hash.decode("UTF-8")
            )

            self.repo.dodaj_osebo(o)

            return

    def obstaja_uporabnik(self, uporabnik: str) -> bool:
        try:
            user = self.repo.dobi_uporabnika(uporabnik)
            return True
        except:
            return False
        
    def prijavi_uporabnika(self, uporabnik : str, geslo_hash: str) -> UporabnikDto | bool :

        # Najprej dobimo uporabnika iz baze
        user = self.repo.dobi_uporabnika(uporabnik)

        geslo_hash_bytes = geslo_hash.encode('utf-8')
        # Ustvarimo hash iz gesla, ki ga je vnesel uporabnik
        succ = bcrypt.checkpw(geslo_hash_bytes, user.password_hash.encode('utf-8'))

        if succ:
            # popravimo last login time
            user.last_login = date.today().isoformat()
            self.repo.posodobi_uporabnika(user)
            return UporabnikDto(username=user.username, role=user.role)
        
        return False
