from operator import attrgetter
class Strumento:  # scrivo la classe Strumento
    def __init__(self, id_strumento, tipo, marca, anno_acquisto, valore):
        self.id = id_strumento
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = int(anno_acquisto)
        self.valore = float(valore)

    def __str__(self):
        return f"{self.id}, {self.tipo}, {self.marca}, {self.anno_acquisto}, {self.valore}"

class Prestito:     # scrivo la classe Prestito
    def __init__(self, id_prestito, data, id_strumento, cognome_allievo):
        self.id = id_prestito
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo

    def __str__(self):
        return f"{self.id}, {self.data}, {self.id_strumento}, {self.cognome_allievo}"



class DepositoStrumenti:        # scrivo la mia classe DepositoStrumenti
    def __init__(self, nome, responsabile):
        self.nome = nome
        self._responsabile = responsabile
        self.strumenti = []     # inizializzo la lista in cui andrò a inserire i miei strumenti
        self.prestiti = []      # inizializzo la lista in cui andrò a inserire i miei strumenti
        self._ultimo_numero_id_strumento = 0 # inizializzo il counter del numero più grande dell'id dello strumento
        self._ultimo_numero_prestito = 0     # inizializzo il counter del numero dell'ultimo prestito

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, nuovo_responsabile):
        self._responsabile = nuovo_responsabile

    def carica_file_strumenti(self, file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as infile:  # apro il file in modalità lettura
                for line in infile:
                    riga_pulita = line.strip()  # pulisco la riga dagli spazi in più
                    campi = riga_pulita.split(",") # la divido in campi splittando con la virgola
                    id_strumento = campi[0]
                    tipo_strumento = campi[1]
                    marca = campi[2]
                    anno = int(campi[3])
                    valore = float(campi[4])

                    s = Strumento(id_strumento, tipo_strumento, marca, anno, valore) # definisco il mio strumento tramite la classe e gli attributi sopra definiti
                    self.strumenti.append(s) # appendo ciascuno strumento trovato alla lista degli strumenti

                    if id_strumento.startswith("S") and id_strumento[1:].isdigit():  #se il codice univoco inizia con "S" e i restanti caratteri sono numerici, allora
                        numero = int(id_strumento[1:])                               # ricavo il numero del codice univoco
                        if numero > self._ultimo_numero_id_strumento:                # se è più grande del counter che avevo aggiornato all'inizio
                            self._ultimo_numero_id_strumento = numero                # allora aggiorno il counter con il numero
        except FileNotFoundError:
            raise FileNotFoundError


    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        self._ultimo_numero_id_strumento += 1 # aumento di uno l'id rispetto all'ultimo numero più grande
        id_nuovo_strumento = f"S{self._ultimo_numero_id_strumento}" # creo l'id del nuovo strumento

        nuovo_strumento = Strumento(id_nuovo_strumento, tipo, marca, anno_acquisto, valore) # creo il nuovo strumento
        self.strumenti.append(nuovo_strumento) # lo appendo alla lista degli strumenti
        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        return sorted(self.strumenti, key=attrgetter("marca"))  # ordino secondo la marca


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        strumento_esistente = False
        for s in self.strumenti:
            if s.id == id_strumento:
                strumento_esistente = True
                break
        if not strumento_esistente:
            raise Exception("Lo strumento non è presente")

        for p in self.prestiti:
            if p.id_strumento == id_strumento:
                raise Exception("Lo strumento è già in prestito")

        self._ultimo_numero_prestito += 1
        id_prestito = f"P{self._ultimo_numero_prestito}"

        nuovo_prestito = Prestito(id_prestito, data, id_strumento, cognome_allievo)
        self.prestiti.append(nuovo_prestito)
        return nuovo_prestito

    def termina_prestito(self, id_prestito):
        for prestito in self.prestiti:
            if prestito.id == id_prestito:
                self.prestiti.remove(prestito)
                return
        raise Exception("Il prestito non esiste")

