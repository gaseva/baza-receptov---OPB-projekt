from data.repository import Repository
import bcrypt
from datetime import date
from data.models import (
    Kategorija,
    Oseba,
    Pripomocek,
    Sestavina,
    SestavinaRecepta,
    Sladica,
    Tezavnost,
)


class UporabnikiService:       

    def registracija(self, ime: str, priimek: str, elektronski_naslov: str, uporabnisko_ime: str, geslo_hash: str):

        if not all([ime, priimek, elektronski_naslov, uporabnisko_ime, geslo_hash,]):
            raise ValueError("Prosim izpolnite vsa polja.")

        if len(geslo_hash) < 8:
            raise ValueError("Geslo mora vsebovati najmanj 8 znakov.")
            
        #zakodiramo geslo
        bytes = geslo_hash.encode('utf-8')
        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(bytes, salt)

        with Repository() as repository:
            if (repository.dobi_osebo_po_uporabniskem_imenu(uporabnisko_ime)
                is not None):
                raise ValueError("To uporabniško ime je že zasedeno.")

            if (repository.dobi_osebo_po_elektronskem_naslovu(elektronski_naslov)
                is not None):
                raise ValueError("Ta elektronski naslov je že registriran.")

            repository.dodaj_osebo(
                ime=ime,
                priimek=priimek,
                elektronski_naslov=elektronski_naslov,
                uporabnisko_ime=uporabnisko_ime,
                geslo_hash=password_hash.decode("UTF-8")
                )


    #  def obstaja_uporabnik(self, uporabnik: str) -> bool:
    #      try:
    #          user = self.repo.dobi_uporabnika(uporabnik)
    #          return True
    #      except:
    #          return False
    #      
    #  def prijavi_uporabnika(self, uporabnik : str, geslo_hash: str) -> UporabnikDto | bool :
#  
    #      # Najprej dobimo uporabnika iz baze
    #      user = self.repo.dobi_uporabnika(uporabnik)
#  
    #      geslo_hash_bytes = geslo_hash.encode('utf-8')
    #      # Ustvarimo hash iz gesla, ki ga je vnesel uporabnik
    #      succ = bcrypt.checkpw(geslo_hash_bytes, user.password_hash.encode('utf-8'))
#  
    #      if succ:
    #          # popravimo last login time
    #          user.last_login = date.today().isoformat()
    #          self.repo.posodobi_uporabnika(user)
    #          return UporabnikDto(username=user.username, role=user.role)
    #      
    #      return False
#  