import numpy as np
from Doppelkopf  import DokoSpiel, Spieler, Strategie_Spieler
import matplotlib.pyplot as plt

from Doppelkopf import Lernender_Spieler


# Simulation mit zufälliger Spielweise und lernenden Spielern

re = 0
kontra = 0
wiederholungen = 10
p1 = [0]
p2 = [0]
p3 = [0]
p4 = [0]

s1 = Spieler('A')
s2 = Spieler('B')
s3 = Spieler('C')
s4 = Lernender_Spieler('Z', './Doppelkopf/model_2.h5', wkeit_zufallszug = 0.25)
# s4 = Spieler('D')
D = DokoSpiel(s1, s2, s3, s4, verbose=False)

for i in range(0, wiederholungen):

    r, k = D.spielen()
    s4.zufallszug = 0.9**i
    re += r
    kontra += k
    p1.append(s1.punkte + p1[-1])
    p2.append(s2.punkte + p2[-1])
    p3.append(s3.punkte + p3[-1])
    p4.append(s4.punkte + p4[-1])
    # if i in [10,20, int(wiederholungen/10), int(2*wiederholungen/10), int(3*wiederholungen/10), int(5*wiederholungen/10), int(9*wiederholungen/10)]:
    #     print(f"+++++++ Runde {i} +++++++++".format())

print(re/wiederholungen, kontra/wiederholungen)

fig, ax = plt.subplots()
x = np.array(range(0,wiederholungen+1))
ax.plot(x, p1)
ax.plot(x, p2)
ax.plot(x, p3)
ax.plot(x, p4)
ax.legend(["Spieler 1", "Spieler 2", "Spieler 3", "Spieler 4"])
plt.show()