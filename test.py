from keras.models import Sequential
from keras.layers import InputLayer
from keras.layers import Dense
from keras.optimizers import adam_v2

model = Sequential()
model.add(InputLayer(input_shape=(1,(24*4+3)*12)))
model.add(Dense(100, activation='sigmoid'))
model.add(Dense(100, activation='sigmoid'))
model.add(Dense(50, activation='relu'))
model.add(Dense(24, activation='linear'))
model.compile(loss='mse', optimizer=adam_v2.Adam(learning_rate=1e-6), metrics=['mae'])

model.save('./Doppelkopf/model_4_Spieler.h5')

# from keras.models import load_model


# model = load_model('./Doppelkopf/model.h5')
# print(model.summary())

import numpy as np

a = np.empty((2,2))
print(a)
# print(np.append(a, np.array([1,2])))

