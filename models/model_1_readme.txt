import numpy as np
import tensorflow as tf

from keras import  layers, models

model = models.Sequential()
model.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(33, 36, 1)))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.Flatten())
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dense(24))

model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=1e-6, beta_1=0.9, beta_2=0.98, 
                                     epsilon=1e-9),
              loss=tf.keras.losses.MeanSquaredError(),
              metrics=['mse'])

model.save('models/model_1.h5')