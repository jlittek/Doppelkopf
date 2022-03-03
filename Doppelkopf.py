from functools import total_ordering
from math import ceil
import random
import numpy as np
from keras.models import load_model


global namen 
namen = {1: 'Herz 9', 2: 'Herz König', 3: 'Herz Ass', 4: 'Pik 9', 5: 'Pik König', 
        6: 'Pik 10', 7: 'Pik Ass', 8: 'Kreuz 9', 9: 'Kreuz König', 10: 'Kreuz 10', 
        11: 'Kreuz Ass', 12: 'Karo 9', 13: 'Karo König', 14: 'Karo 10', 15: 'Karo Ass', 
        16: 'Karo Bube', 17: 'Herz Bube', 18: 'Pik Bube', 19: 'Kreuz Bube', 20: 'Karo Dame',
        21: 'Herz Dame', 22: 'Pik Dame', 23: 'Kreuz Dame', 24: 'Herz 10'}
global farben
farben = {1: 'Herz', 2: 'Herz', 3: 'Herz', 4:'Pik', 5:'Pik', 6:'Pik', 7: 'Pik', 8: 'Kreuz', 
    	9:'Kreuz', 10: 'Kreuz', 11:'Kreuz'}
global augenzahlen
augenzahlen = {1: 0, 2: 4, 3: 11, # Herz
                4: 0, 5: 4, 6: 10, 7: 11, # Pik
                8: 0, 9: 4, 10: 10, 11: 11, # Kreuz
                12: 0, 13: 4, 14: 10, 15:11, # Karo
                16: 2, 17: 2, 18: 2, 19: 2, # Buben
                20: 3, 21: 3, 22: 3, 23: 3, # Damen
                24: 10} # Herz 10

@total_ordering
class Karte:

    def __init__(self, id) -> None:
        self.id = id
        if farben.get(id) == None:
            self.farbe = 'Trumpf'
        else :
            self.farbe = farben.get(id)
        self.augenzahl = augenzahlen.get(id)

    def __str__(self) -> str:
        return namen[self.id]

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __gt__(self, other):
        return self.id > other.id
    
    def __repr__(self):
        return str(self)
    
    def __add__(self, other):
        if type(other).__name__ == 'Karte':
            return self.augenzahl + other.augenzahl
        else:
            return self.augenzahl + other
    
    def __radd__(self, other):
        if other == 0:
            return self
        else: 
            return self.__add__(other)

class Kartenspiel:
    def __init__(self) -> None:
        self.karten = []
        for i in namen:
            self.karten.append(Karte(i))
            self.karten.append(Karte(i))

    def geben(self):
        gemischte_Karten = random.sample(self.karten, len(self.karten))
        return gemischte_Karten[0:12], gemischte_Karten[12:24], gemischte_Karten[24:36], gemischte_Karten[36:48]

class DokoSpiel:
    
    def __init__(self, spieler_1, spieler_2, spieler_3, spieler_4, verbose = False) -> None:
        Karten = Kartenspiel()
        a, b, c, d = Karten.geben()
        l = [a,b,c,d]
        self.spieler = [spieler_1, spieler_2, spieler_3, spieler_4]
        for s, k in zip(self.spieler, l):
            s.karten_aufnehmen(k)
            s.set_spielreferenz(self)
        self.aktueller_stich = []
        self.alle_stiche = []
        self.verbose = verbose
        self.zustand = np.zeros((24*4+1, 12))


    def get_aktueller_stich(self):
        return self.aktueller_stich

    def get_letzter_stich(self):
        return self.alle_stiche[-1]
    
    def karte_ablegen(self, karte):
        self.aktueller_stich.append(karte)
        if len(self.aktueller_stich) == 4:
            self.alle_stiche.append(self.aktueller_stich)
            self.aktueller_stich = []

    def spielen(self):

        # eventuelle Punkte aus vorigen Runden löschen:
        for s in self.spieler:
            s.punkte = 0
            s.augen = 0

        for i in range(1,13):
            if self.verbose: print(f"{i}. Stich:".format())
            # Runde in Zustand aktualisieren:
            self.zustand[0] = np.identity(12)[i-1]

            for s in self.spieler:
                karte = s.spielen(verbose = self.verbose)
                self.aktueller_stich.append(karte)
                # gespielte Karten in Zustand aktualisieren:
                i2 = self.spieler.index(s)
                j = np.argmax(self.zustand[0])
                neu = np.zeros(24)
                neu[karte.id-1] = 1
                self.zustand[i2*24+1:i2*24+24+1, j] = neu
            # Stich auswerten, Punkte verteilen, neue Reihenfolge festlegen
            wert_aktueller_stich = sum(self.aktueller_stich)
            # Gewinner des Stichs ermitteln
            gewinner_id = self.wer_bekommt_den_stich()
            if self.verbose: print(f"Der {i}. Stich hat eine Augenzahl von {wert_aktueller_stich}, Spieler {self.spieler[gewinner_id].name} gewinnt den Stich.".format())
            # Augen dem Gewinner gutschreiben:
            self.spieler[gewinner_id].augen += wert_aktueller_stich
            # neue Zugreihenfolge festlegen:
            for i in range(0,gewinner_id):
                self.spieler.append(self.spieler.pop(0))
            # aktuellen Stich in die Liste einfügen und zurücksetzen:
            self.alle_stiche.append(self.aktueller_stich)
            self.aktueller_stich = []

            # für alle lernenden Spieler Reward zurückgeben, um deren Gewichte anpassen zu können
            # for s in self.spieler:
            #     if type(s).__name__ == "Lernender_Spieler":
            #         if self.spieler.index(s) == gewinner_id:
            #             s.update(wert_aktueller_stich)
            #         else:
            #             s.update(0)



        # Ende des Spiels, Punkte zusammenzählen:
        re = 0
        kontra = 0
        for i in range(0,4):
            if self.spieler[i].re_partei:
                re += self.spieler[i].augen
            else:
                kontra += self.spieler[i].augen
        sieger, siegpunkte = self.sieger_ermitteln(re, kontra)
        if self.verbose: 
            print(f"Spieler {self.spieler[0].name}: {self.spieler[0].augen}, Spieler {self.spieler[1].name}: {self.spieler[1].augen}, Spieler {self.spieler[2].name}: {self.spieler[2].augen}, Spieler {self.spieler[3].name}: {self.spieler[3].augen}".format())
            print(f"Re-Partei: {re} Augen, Kontra: {kontra} Augen, es gewinnt {sieger} mit {siegpunkte} Punkten.".format())
        
        # Spiel zurücksetzen:
        self.__init__(self.spieler[0], self.spieler[1],self.spieler[2],self.spieler[3], self.verbose)

        if sieger == "Re":
            for i in range(0,4):
                if self.spieler[i].re_partei:
                    self.spieler[i].punkte  = siegpunkte
                else:
                    self.spieler[i].punkte = 0 # -siegpunkte
                if type(self.spieler[i]).__name__ == "Lernender_Spieler":
                    self.spieler[i].update()
                    self.spieler[i].modell_speichern()

            return siegpunkte, 0 # siegpunkte, -siegpunkte
        else:
            for i in range(0,4):
                if not self.spieler[i].re_partei:
                    self.spieler[i].punkte  = siegpunkte
                else:
                    self.spieler[i].punkte = 0 # -siegpunkte
                if type(self.spieler[i]).__name__ == "Lernender_Spieler":
                    self.spieler[i].update()
                    self.spieler[i].modell_speichern()
                    

            return 0, siegpunkte # -siegpunkte, siegpunkte




    def wer_bekommt_den_stich(self) -> int:
        # Farb oder Trumpfstich?:
        if self.aktueller_stich[0].farbe == 'Trumpf':
            id = np.argmax(self.aktueller_stich)
            return id
        else: # Farbstich:
            # wurde gestochen?
            if max(self.aktueller_stich) > Karte(11):
                return np.argmax(self.aktueller_stich)
            else: # es wurde nicht gestochen:
                farbe = self.aktueller_stich[0].farbe
                # alle Karten die richtig bekannt haben:
                kandidaten = filter(lambda karte: karte.farbe == farbe, self.aktueller_stich)
                hoechste_karte = max(kandidaten)
                return self.aktueller_stich.index(hoechste_karte)

    def sieger_ermitteln(self, re, kontra):
        if re > kontra:
            return "Re", ceil(re / 30 - 4)
        else:
            return "Kontra", ceil(kontra / 30 - 4) + 1 # +1 "gegen die Alten"

    def get_zustand(self, spieler):
        zustand = self.zustand
        karten = spieler.handkarten
        karten_als_array = np.zeros(24)
        for k in karten:
            karten_als_array[k.id-1] += 1
        
        return np.append(zustand, karten_als_array.reshape((2,12)))

class Spieler:

    def __init__(self, name) -> None:
        self.name = name
        self.augen = 0
        self.re_partei = False
        self.punkte = 0

    def karten_aufnehmen(self, karten):
        self.handkarten = karten
        self.handkarten.sort()
        self.re_partei = (Karte(23) in self.handkarten) # Karte(23) ist Kreuz-Dame

    def karte_spielen(self, karte):
        self.handkarten.remove(karte)

    def set_spielreferenz(self, spiel: DokoSpiel) -> None:
        self.spiel = spiel

    def spielen(self, verbose = False) -> Karte:
        # legale Karten ermitteln:
        legale_karten = self.legale_karten_ermitteln()
        # spiele eine zufällige legale Karte:
        id = random.randint(1, len(legale_karten)) - 1 
        karte = legale_karten[id]
        if verbose: print(self.name, karte)
        self.karte_spielen(karte)
        return karte

    def legale_karten_ermitteln(self):
        aktueller_stich = self.spiel.aktueller_stich
        # falls aktueller Stich noch leer, sind alle Karten erlaubt:
        if len(aktueller_stich) == 0:
            return self.handkarten
        else:
            erg = list(filter(lambda karte: karte.farbe == aktueller_stich[0].farbe, self.handkarten))
            if len(erg) == 0:
                return self.handkarten
            else:
                return erg

    def __str__(self) -> str:
        return str(self.handkarten)

    def __repr__(self) -> str:
        return str(self.handkarten)

class Strategie_Spieler(Spieler):

    def __init__(self, name) -> None:
        super().__init__(name)

    def spielen(self, verbose = False):
        # legale Karten ermitteln:
        legale_karten = self.legale_karten_ermitteln()
        # spiele höchste Karte
        karte = legale_karten[-1]
        if verbose: print(self.name, karte)
        self.karte_spielen(karte)
        return karte

class Menschlicher_Spieler(Spieler):

    def __init__(self, name) -> None:
        super().__init__(name)
    
    def spielen(self, verbose=False) -> Karte:
        print(self.handkarten)
        id = int(input())
        karte = self.handkarten[id]
        print(self.name, karte)
        self.karte_spielen(karte=karte)
        return karte

class Lernender_Spieler(Spieler):
    
    def __init__(self, name, path='path/to/location/of/model', wkeit_zufallszug=0.25) -> None:
        # Model laden
        self.model = load_model(path)
        self.path = path
        self.zufallszug = wkeit_zufallszug
        self.trajektorie = [] # Liste mit Zustand in jedem Zug, Vorhersage und ausgewählter Aktion
        super().__init__(name)

    def spielen(self, verbose=False) -> Karte:

        legale_karten = self.legale_karten_ermitteln()
        # erhalte aktuellen Zustand
        zustand = self.spiel.get_zustand(self)
        # bekomme von Model Vorhersage für jede Aktion
        vorhersage = self.model.predict(zustand.reshape((1,33,36,1))).reshape(24)
        # mit Wahrscheinlichkeit self.zufallszug spiele zufällige Karte:
        if random.random() < self.zufallszug:
            id = random.randint(1, len(legale_karten)) - 1 
            karte = legale_karten[id]
            if verbose: print(self.name, karte)
            self.karte_spielen(karte)
            # erweitere Trajektorie
            self.trajektorie.append([zustand, vorhersage, karte.id])
            return karte
        else:
            vorhersage_kopie = vorhersage
            # print(vorhersage)
            # wähle legale Aktion mit maximalem Reward in der Vorhersage 
            while not Karte(np.argmax(vorhersage)+1) in legale_karten:
                vorhersage[np.argmax(vorhersage)] = -2*abs(np.min(vorhersage))
            karte = Karte(np.argmax(vorhersage)+1)
            self.karte_spielen(karte)
            if verbose: print(self.name, karte)
            # erweitere Trajektorie:
            self.trajektorie.append([zustand, vorhersage_kopie, karte.id])
            return karte

    def update(self):
        # update Model mit dem Reward und der zuvor ausgeführten Aktion
        # y = self.letzte_vorhersage
        # y[self.letzte_aktion - 1] = reward
        # self.model.fit(self.letzter_zustand.reshape(1,1,(24*4+3)*12), y.reshape(1,1,24))

        # neu: update nach dem Spiel für alle Züge
        #  i. Stich  wird belohnt mit:
        # reward = augen_i/30 * 0.5^i + siegpunkte * 1/0.5^i
        # oder
        # reward = augen_i/30 * (1 - i/12) + siegpunkte * i/12
        # oder 
        # reward = augen_i *  0.9^i + siegpunkte * 0.9^(12-i)
        # oder am besten
        # reward = siegpunkte 
        self.model = load_model(self.path)
        alle_x = []
        alle_y = []
        for t in self.trajektorie:
            zustand = t[0]
            alle_x.append([zustand.reshape((1,33,36,1))])
            y = t[1]
            letzte_aktion = t[2]
            y[letzte_aktion - 1] = self.punkte # = reward
            alle_y.append([y.reshape(1,24)])
        self.model.fit(np.array(alle_x).reshape(12,33,36,1), np.array(alle_y).reshape(12,1,24), epochs=1)
        self.trajektorie = []
        self.model.save(self.path)

    def modell_speichern(self):
        pass





        
