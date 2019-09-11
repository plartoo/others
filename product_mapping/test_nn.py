import pdb

import keras
import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
from keras.utils import np_utils
from sklearn.preprocessing import LabelEncoder

## Generate dummy data
# import numpy as np
# x_train = np.random.random((1000, 20))
# y_train = keras.utils.to_categorical(np.random.randint(10, size=(1000, 1)), num_classes=10)
# x_test = np.random.random((100, 20))
# y_test = keras.utils.to_categorical(np.random.randint(10, size=(100, 1)), num_classes=10)

seed = 7
numpy.random.seed(seed)

# load dataset
dataframe = pandas.read_csv("./input/raw_mappings.csv", header=None) # numpy.loadtxt('./input/raw_mappings.csv', delimiter=',')
dataset = dataframe.values
X_len = len(dataset[0,:-1]) # input channels
X = dataset[:,0:X_len].astype(float)
Y = dataset[:,X_len]
Y_cnt = len(numpy.unique(Y))

# encode class values as integers
encoder = LabelEncoder()
encoder.fit(Y)
encoded_Y = encoder.transform(Y)
# convert integers to dummy variables (i.e. one hot encoded)
dummy_y = np_utils.to_categorical(encoded_Y)

model = Sequential()
# Dense(64) is a fully-connected layer with 64 hidden units.
# in the first layer, you must specify the expected input data shape:
# here, 20-dimensional vectors.
model.add(Dense(64, activation='relu', input_dim=20))
model.add(Dropout(0.5))
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
model.compile(loss='categorical_crossentropy',
              optimizer=sgd,
              metrics=['accuracy'])

model.fit(x_train, y_train,
          epochs=20,
          batch_size=128)
score = model.evaluate(x_test, y_test, batch_size=128)

