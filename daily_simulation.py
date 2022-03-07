from datetime import datetime
import pandas as pd
from Doppelkopf import DokoSpiel, Spieler, Lernender_Spieler
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model


# set up 3 learning agents and 1 random player:
path = 'models/model_2.h5'
model = load_model(path)
player_1 = Lernender_Spieler('Player 1', model)
player_2 = Lernender_Spieler('Player 2', model)
player_3 = Lernender_Spieler('Player 3', model)
player_4 = Spieler('Player 4')

# set up a game instance and assign the players:
game = DokoSpiel(player_1, player_2, player_3, player_4)

# let the agents play several repetitions and save their scores:
repetitions = 1000
score_player_1 = []
score_player_2 = []
score_player_3 = []
score_player_4 = []
for r in range(0, repetitions):
    re, kontra = game.spielen()
    score_player_1.append(player_1.punkte)
    score_player_2.append(player_2.punkte)
    score_player_3.append(player_3.punkte)
    score_player_4.append(player_4.punkte)

model.save(path)

dates = np.full((repetitions), datetime.today().date())
scores = pd.read_csv('simulation_scores/scores_2.csv')
new_scores = pd.DataFrame({'Date': dates, 'Player 1': score_player_1, 'Player 2': score_player_2, 'Player 3': score_player_3, 'Player 4': score_player_4})
scores = pd.concat([scores, new_scores])
scores.to_csv('simulation_scores/scores_2.csv', index = False)

cumsum = scores[['Player 1', 'Player 2', 'Player 3', 'Player 4']].cumsum()
fig = plt.plot(cumsum)
plt.legend(cumsum.columns)
plt.xlabel('Games')
plt.ylabel('Total points')
plt.savefig('simulation_scores/scores_2.pdf')
