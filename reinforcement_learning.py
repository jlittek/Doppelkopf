import numpy as np
from keras.models import Sequential
from keras.layers import InputLayer
from keras.layers import Dense

model = Sequential()
model.add(InputLayer(batch_input_shape=(1, env.observation_space.n)))
model.add(Dense(20, activation='relu'))
model.add(Dense(env.action_space.n, activation='linear'))
model.compile(loss='mse', optimizer='adam', metrics=['mae'])

# discount_factor = 0.95
# eps = 0.5
# eps_decay_factor = 0.999
# num_episodes=500