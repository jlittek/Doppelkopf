import pandas as pd
import numpy as np
import datetime
rep = 1
dates = np.full((rep), datetime.datetime.today().date())



scores = pd.DataFrame({'Date': dates, 'Player 1': [0], 'Player 2': [0], 'Player 3': [0], 'Player 4': [0]})
# new_scores = pd.DataFrame({'Date': dates,'Player 1': [1], 'Player 2': [2], 'Player 3': [3], 'Player 4': [4]})
# scores = pd.concat([scores, new_scores])
scores.to_csv('simulation_scores/scores.csv', index=False)