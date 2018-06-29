from libraries import *
import numpy as np
import pandas as pd
import keras.backend as K
from keras.models import Sequential
from keras.layers import Dense, Conv2D, LSTM


def to_categorical(x):
    n = len(set(x))
    N = x.shape[0]
    tmp = np.array([np.zeros(n) for i in range(N)])
    for n,i in enumerate(x): tmp[n][i]=1
    return tmp

Xtrain = load_MNIST_images('train-images-idx3-ubyte').T
Xtest = load_MNIST_images('t10k-images-idx3-ubyte').T
Xtrain = Xtrain.reshape(Xtrain.shape[0],-1,1)
Xtest = Xtest.reshape(Xtest.shape[0],-1,1)

ytrain = to_categorical(open_binary('train-labels-idx1-ubyte')[8:])
ytest = to_categorical(open_binary('t10k-labels-idx1-ubyte')[8:])


# build the model
model = Sequential()
model.add(LSTM(32, input_shape=(Xtrain.shape[1:])))
model.add(Dense(10, activation='softmax'))

# compile the model
model.compile(loss='categorical_crossentropy',
			  optimizer='rmsprop',
			  metrics=['accuracy'])

model.fit(Xtrain, ytrain,
		  batch_size=128,
		  epochs=100,
		  validation_split=0.3,
		  verbose=0)

