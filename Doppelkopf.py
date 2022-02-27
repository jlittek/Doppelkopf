from functools import total_ordering
from math import ceil
import random
import numpy as np

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
        for i in range(1,13):
            if self.verbose: print(f"{i}. Stich:".format())
            for s in self.spieler:
                self.aktueller_stich.append(s.spielen(verbose = self.verbose))
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
        if sieger == "Re":
            for i in range(0,4):
                if self.spieler[i].re_partei:
                    self.spieler[i].punkte  = siegpunkte
            return siegpunkte, 0
        else:
            for i in range(0,4):
                if not self.spieler[i].re_partei:
                    self.spieler[i].punkte  = siegpunkte
            return 0, siegpunkte

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

class environment:

    def __init__(self) -> None:
        self.state = np.zeros((12*4+2+1, 12))
        self.done = False
        self.current_round = 0
        self.all_tricks = []
        self.current_trick = []

    def step(self, action):
        player_id = action.player_id
        card_to_play = action.card_to_play
        hand_cards = action.hand_cards

        reward = 0
        if len(self.current_trick) == 4:
            self.current_trick = []

        # action is a 24 x 1 array, wich indicates which card should be played
        # state is a (24*4 + 2 + 1) x 12 array giving information about all played 
        # cards of all players and the remaining own cards and the current round

        # do action
        self.state[(player_id*12 - 1):(player_id*12 + 11), self.current_round] = card_to_play
        self.state[96:98,0:12] = hand_cards

        # compute rewards
        # decide first if a trump has to be played:
        trump_trick = False

        try:
            trump_trick = self.current_trick[0] > 11
        except:
            # trick is empty, therefore any card is allowed:
            self.current_trick.append(card_to_play.index(1) + 1)
            return self.state, reward, self.done

        # update the current trick:
        self.current_trick.append(card_to_play.index(1) + 1)
        if len(self.current_trick) == 4:
            self.current_round +=1
            self.state[-1, (self.current_round - 2, self.current_round)] = [0,1]
        # not playing trump although the player still has trump:
        if trump_trick and (self.current_trick[-1] < 11) and (hand_cards.max() > 11):
            reward = -9999
            self.done = True

        # not following although the player has to follow in non-trump:
        if not trump_trick and self.must_follow(self.current_trick[0], card_to_play, hand_cards):
            reward = -9999
            self.done = True

        if self.current_round == 12:
            self.done = True
        return self.state, reward, self.done

    def must_follow(first_card, own_card, hand_cards) -> bool:
        if (first_card in [1,2,3]) and not (own_card in [1,2,3]) and (len(set(hand_cards) & set([1,2,3])) > 0):
            return True
        if (first_card in [4,5,6,7]) and not (own_card in [4,5,6,7]) and (len(set(hand_cards) & set([4,5,6,7])) > 0):
            return True
        if (first_card in [8,9,10,11]) and not (own_card in [8,9,10,11]) and (len(set([hand_cards]) & set([8,9,10,11])) > 0):
            return True
        return False

class action:
    def __init__(self, hand_cards, card_to_play, player_id) -> None:
        self.hand_cards = hand_cards
        self.cars_to_play = card_to_play
        self.player_id = player_id




        
