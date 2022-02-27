import matplotlib
import numpy as np
from Doppelkopf  import DokoSpiel, Spieler, Strategie_Spieler
import matplotlib.pyplot as plt


# Simulation mit zufälliger Spielweise

re = 0
kontra = 0
wiederholungen = 1000
p1 = [0]
p2 = [0]
p3 = [0]
p4 = [0]

for i in range(0, wiederholungen):
    s1 = Spieler('A')
    s2 = Spieler('B')
    s3 = Spieler('C')
    s4 = Spieler('D')
    D = DokoSpiel(s1, s2, s3, s4)
    r, k = D.spielen()
    re += r
    kontra += k
    p1.append(s1.punkte + p1[-1])
    p2.append(s2.punkte + p2[-1])
    p3.append(s3.punkte + p3[-1])
    p4.append(s4.punkte + p4[-1])

print(re/wiederholungen, kontra/wiederholungen)

fig, ax = plt.subplots()
x = np.array(range(0,wiederholungen+1))
ax.plot(x, p1)
ax.plot(x, p2)
ax.plot(x, p3)
ax.plot(x, p4)
ax.legend(["Spieler 1", "Spieler 2", "Spieler 3", "Spieler 4"])
plt.show()