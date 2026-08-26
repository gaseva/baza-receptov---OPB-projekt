from data.repository import Repository
import bcrypt
from data.models import Oseba


class UporabnikiService:       

    def registracija(self, ime: str, priimek: str, elektronski_naslov: str, uporabnisko_ime: str, geslo: str) -> Oseba:

        if not all([ime, priimek, elektronski_naslov, uporabnisko_ime, geslo]):
            raise ValueError("Prosim izpolnite vsa polja.")

        if len(geslo) < 8:
            raise ValueError("Geslo mora vsebovati najmanj 8 znakov.")
            
        #zakodiramo geslo
        geslo_bytes = geslo.encode('utf-8')
        salt = bcrypt.gensalt()
        geslo_hash = bcrypt.hashpw(geslo_bytes, salt)

        with Repository() as repository:
            if (repository.dobi_osebo_po_uporabniskem_imenu(uporabnisko_ime)
                is not None):
                raise ValueError("To uporabniško ime je že zasedeno.")

            if (repository.dobi_osebo_po_elektronskem_naslovu(elektronski_naslov)
                is not None):
                raise ValueError("Ta elektronski naslov je že registriran.")

            oseba = repository.dodaj_osebo(
                ime=ime,
                priimek=priimek,
                elektronski_naslov=elektronski_naslov,
                uporabnisko_ime=uporabnisko_ime,
                geslo_hash=geslo_hash.decode("UTF-8")
                )
            return oseba

        
    def prijava(self, uporabnisko_ime: str, geslo: str) -> Oseba:
            if not uporabnisko_ime or not geslo:
                raise ValueError("Prosim izpolnite vsa polja.")
            
            with Repository() as repository:
                uporabnisko_ime = uporabnisko_ime.strip()
                # dobimo uporabnika iz baze po uporabniškem imenu (dobimo objekt Oseba)
                user = repository.dobi_osebo_po_uporabniskem_imenu(uporabnisko_ime)
                
                #preverimo ali obstraja uporabnik
                if user is None:
                    raise ValueError("Uporabniško ime ali geslo je napačno.")
                
                #preverimo ujemanje gesel
                try:
                    pravilno_geslo = bcrypt.checkpw(
                        geslo.encode("utf-8"),
                        user.geslo_hash.encode("utf-8"),
                    )
                except (ValueError, TypeError):
                    pravilno_geslo = False

                if not pravilno_geslo:
                    raise ValueError(
                        "Uporabniško ime ali geslo je napačno."
                    )

                return user
            
            
    def priljubljeni_recepti(self, oseba_id: int):
        with Repository() as repository:
            priljubljeno = repository.dobi_priljubljene_recepte(oseba_id)
            return priljubljeno
                
                

        
 