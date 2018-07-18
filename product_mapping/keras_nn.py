import pdb
import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import LabelEncoder


## define baseline model
# def baseline_model():
#     # create model
#     model = Sequential()
#
#     # TODO: change NN layer config
#     model.add(Dense(100, input_dim=X_len, activation='relu'))
#     model.add(Dense(Y_cnt, activation='softmax'))
#
#     # Compile model
#     model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#     return model
## a bit of an unusual flow for Keras
# estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5, verbose=0)
# kfold = KFold(n_splits=10, shuffle=True, random_state=seed)
# results = cross_val_score(estimator, X, dummy_y, cv=kfold)
# print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))


# fix random seed for reproducibility
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

# create model
model = Sequential()
model.add(Dense(100, input_dim=X_len, activation='relu')) # TODO: change NN layer config
model.add(Dense(Y_cnt, activation='softmax'))
# Compile model
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X, Y, epochs=150, batch_size=10000, verbose=1)

# serialize model to JSON
model_json = model.to_json()
with open("model.json", "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("model.h5")
print("Saved model to disk")

## to use this later...
## https://machinelearningmastery.com/save-load-keras-deep-learning-models/
## load json and create model
# json_file = open('model.json', 'r')
# loaded_model_json = json_file.read()
# json_file.close()
# loaded_model = model_from_json(loaded_model_json)
# # load weights into new model
# loaded_model.load_weights("model.h5")
# print("Loaded model from disk")
#
# # evaluate loaded model on test data
# loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
# score = loaded_model.evaluate(X, Y, verbose=0)
# print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1] * 100))

# TODO:
# Try this: Multilayer Perceptron (MLP) for multi-class softmax classification
# https://keras.io/getting-started/sequential-model-guide/
# http://www.riptutorial.com/tensorflow/example/30750/math-behind-1d-convolution-with-advanced-examples-in-tf
# https://www.tensorflow.org/tutorials/estimators/cnn
