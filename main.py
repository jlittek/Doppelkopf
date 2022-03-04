import numpy as np
from Doppelkopf  import DokoSpiel, Spieler, Lernender_Spieler
import matplotlib.pyplot as plt



# Simulation mit zufälliger Spielweise und lernenden Spielern

re = 0
kontra = 0
wiederholungen = 200
x = np.array(range(1, wiederholungen + 2))
p1 = np.zeros(wiederholungen+1)
p2 = np.zeros(wiederholungen+1)
p3 = np.zeros(wiederholungen+1)
p4 = np.zeros(wiederholungen+1)

s1 = Lernender_Spieler('A', 'cnn_1.h5', wkeit_zufallszug = 0.25)
s2 = Lernender_Spieler('B', 'cnn_1.h5', wkeit_zufallszug = 0.25)
s3 = Lernender_Spieler('C', 'cnn_1.h5', wkeit_zufallszug = 0.25)
# s1 = Spieler('A')
# s2 = Spieler('B')
# s3 = Spieler('C')
# s4 = Lernender_Spieler('D', './Doppelkopf/model_4_Spieler.h5', wkeit_zufallszug = 0.25)
s4 = Spieler('D')
D = DokoSpiel(s1, s2, s3, s4, verbose=False)

plt.ion()
figure, ax = plt.subplots(figsize=(2, 2))
line1, = ax.plot(x, p1, 'g-')
line2, = ax.plot(x, p2, 'r-')
line3, = ax.plot(x, p3, 'y-')
line4, = ax.plot(x, p4, 'b-')
ax.legend(["Spieler 1", "Spieler 2", "Spieler 3", "Spieler 4"])

# setting x-axis label and y-axis label
plt.xlabel("Spiel")
plt.ylabel("Punkte")
plt.ylim(0, 2*wiederholungen)

for i in range(0, wiederholungen):

    r, k = D.spielen()
    # s4.zufallszug = 0.99**i
    re += r
    kontra += k
    p1[i+1] = s1.punkte + p1[i]
    p2[i+1] = s2.punkte + p2[i]
    p3[i+1] = s3.punkte + p3[i]
    p4[i+1] = s4.punkte + p4[i]

    line1.set_ydata(p1)
    line2.set_ydata(p2)
    line3.set_ydata(p3)
    line4.set_ydata(p4)
    figure.canvas.draw()
    figure.canvas.flush_events()

    # if i in [10,20, int(wiederholungen/10), int(2*wiederholungen/10), int(3*wiederholungen/10), int(5*wiederholungen/10), int(9*wiederholungen/10)]:
    #     print(f"+++++++ Runde {i} +++++++++".format())

print(re/wiederholungen, kontra/wiederholungen)

# fig, ax = plt.subplots()
# x = np.array(range(0,wiederholungen+1))
# ax.plot(x, p1)
# ax.plot(x, p2)
# ax.plot(x, p3)
# ax.plot(x, p4)
# ax.legend(["Spieler 1", "Spieler 2", "Spieler 3", "Spieler 4"])
plt.savefig(f'./Doppelkopf/3_hidden_3v1_Spieler_cnn_{wiederholungen}.png'.format())
# plt.show()