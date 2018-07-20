import pdb

import time

import numpy
import pandas
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.models import model_from_json
from keras.wrappers.scikit_learn import KerasClassifier
from keras.utils import np_utils
from keras.optimizers import SGD, RMSprop, Adagrad, Adadelta, Adam, Adamax, Nadam, TFOptimizer
from sklearn.model_selection import cross_val_score, train_test_split, KFold
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
stamp = str(int(time.time()))

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

# split into 80-20 for training and testing
X_train, X_test, Y_train, Y_test = train_test_split(X, dummy_y, test_size=0.2, random_state=seed)

# create model
model = Sequential()
activation_func = 'softplus'
model.add(Dense(X_len+X_len,#int(X_len/2),
                input_dim=X_len, activation=activation_func)) # fully-connected layer with X_len/2 hidden units
model.add(Dropout(0.5))
#softmax; elu; selu; softplus; softsign; relu; tanh; sigmoid; hard_sigmoid; linear
model.add(Dense(X_len+X_len, activation=activation_func)) # softmax/softplus(38%); elu/selu/relu(38%);
model.add(Dropout(0.5))
model.add(Dense(X_len+X_len, activation=activation_func))
model.add(Dropout(0.5))
# softplus-softplus-40p; softmax-softmax-38p; softsign-softsign-02%;
# tanh-tanh-02%; sigmoid-sigmoid-38p; hard_sigmoid-hard_sigmoid-0.2p; linear-linear-5%;
model.add(Dense(Y_cnt, activation=activation_func))
# serialize model to JSON
model_json = model.to_json()
with open("model_"+stamp+".json", "w") as json_file:
    json_file.write(model_json)

## Compile model
# Optimizers: https://keras.io/optimizers/
#sgd; RMSprop; Adagrad; Adadelta Adam; Adamax; Nadam
sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9, nesterov=True)
rmsprop = RMSprop(lr=0.001, rho=0.9, epsilon=None, decay=0.0)
adagrad = Adagrad(lr=0.01, epsilon=None, decay=0.0)
adadelta = Adadelta(lr=1.0, rho=0.95, epsilon=None, decay=0.0)
adam = Adam(lr=0.001, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)
adamax = Adamax(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0)
nadam = Nadam(lr=0.002, beta_1=0.9, beta_2=0.999, epsilon=None, schedule_decay=0.004)
# TODO: learn how to use TFOptimizer(optimizer)
model.compile(loss='categorical_crossentropy',
              # optimizer='adam', # 35% accuracy
                optimizer=adamax,
              # [sgd is Meh] sgd 46% at epoch 100; with Xlen+Xlen, Xlen+Xlen, Xlen+Xlen, softplus gets 60% at 100ep
              # [rmsprop is BAD; it forgets easily and quickly] rmsprop 48% only at epoch 19 and after is bad;
              # [adagrad does NOT perform in wide networks] adagrad 48% at epoch 100; stalled at just 38% for (Xlen+Xlen)*3 config
              # [NEVER USE THIS/adadelta] adadelta learns faster and reaches 46% at just epoch 39, but dropps off afterward; if we use X_len as second hidden layer and use adadelta, it peaks at 47% at epoch 34
              # ** adam goes up to 48% at epoch 100; adamax goes up to 49% at epoch 100, has a lot of potential for longer epoch
              # [adam is just okay] adam with 3*(Xlen+Xlen) peaked at 60% and is slow
              # [nadam is BAD; never goes up from 38% for wide nets like 3*(Xlen+Xlen)] nadam tops at 46% after 100 epoch

                # adamax with X_len, 100, and softplus gets 54% at epoch 100
              # adamax with X_len , X_len, softplus gets 56% at 100 ep
              # adamax with X_len, X_len, X_len, softplus gets 55% at 100 ep
              # adamax with Xlen, Xlen+Xlen, Xlen, softplus gets 58% at 100ep and has potential to go a bit higher
              # adamax with Xlen+Xlen, Xlen+Xlen, Xlen, softplus gets 65% at 100ep
              # adamax with Xlen+Xlen, Xlen+Xlen, Xlen+Xlen, softplus gets 66% at 100ep
                # adamax with Xlen+Xlen, Xlen+Xlen, Xlen+Xlen, softplus gets 64% at 100ep WITH batch size 100

              metrics=['accuracy'])
# REF: https://machinelearningmastery.com/evaluate-performance-deep-learning-models-keras/
# https://keras.io/getting-started/sequential-model-guide/
batch_size = 100
model.fit(X_train, Y_train, epochs=100, batch_size=batch_size, verbose=1)
score = model.evaluate(X_test,Y_test, batch_size=batch_size)
print(score)
# serialize weights to HDF5
model.save_weights("model_"+stamp+".h5")
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
# Look at example below and see if I can replicate similar Tensorflow in Keras:
# https://github.com/keras-team/keras/issues/7818
# Convolution layer: https://keras.io/layers/convolutional/
# Try this: Multilayer Perceptron (MLP) for multi-class softmax classification
# https://keras.io/getting-started/sequential-model-guide/
# http://www.riptutorial.com/tensorflow/example/30750/math-behind-1d-convolution-with-advanced-examples-in-tf
# https://www.tensorflow.org/tutorials/estimators/cnn
