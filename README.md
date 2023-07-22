# Learning Doppelkopf with reinforcement learning and artificial neural networks

![Scores](simulation_scores/scores.jpg?raw=true "Total scores")

## Problem/Task:
Build (very) strong computer opponents for the game with reinforcement learning. 

## Approach:
Therefore the game rules have been implemented in Python. There are different types of computer players: Each can play the game, the simple class 'Spieler' plays in each trick a random card, but only one of the allowed cards for each trick. This means, he knows the rules, but is a very bad player. The class 'Lernender_Spieler' (learning player) is a sub class of the former. He chooses his cards by a recommendation from a CNN (or any other model). After each hand/game he updates these recommendations by training the CNN with the final reward of this hand. With probability 0.25 he also draws randomly. 
In the current setup tree learning players play with one random player, using and training the same model. Their cumulated scores are shown n the graphic above. If the learning is successful, the curve of player 4, the random player, should increase slower at some point. Since 2022-03-05 a total of 24000 games is played per day.

## To-do for the case the learning is successful:
Modify the game to allow for special rules and implement a GUI for interaction with human players.

Needed special rules for this case:
- extra points for foxes, Doko, Charlie
- wedding
- calling (Re, Kontra)
- poverty
- other special rules

