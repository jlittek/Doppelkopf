from Doppelkopf import DokoSpiel, Menschlicher_Spieler, Spieler


s1 = Menschlicher_Spieler('J')
s2 = Spieler('A')
s3 = Spieler('B')
s4 = Spieler('C')
D = DokoSpiel(s1, s2, s3, s4, verbose=True)
D.spielen()