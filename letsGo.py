import tensorflow as tf
import tflearn

import speech_data

import numpy as np


from constants import POSITIVE_PATH, NEGATIVE_PATH



learning_rate = 0.03
training_iters = 10  # steps
batch_size = 2

width = 1
height = 8192  # (max) length of utterance
classes = 1  # digits

positive_batch = word_batch = speech_data.wave_batch_generator(batch_size, POSITIVE_PATH, 1)
negative_batch = word_batch = speech_data.wave_batch_generator(batch_size, NEGATIVE_PATH, 0)
#positive_batch = np.reshape(positive_batch, (1, 10, 8192))
#negative_batch = np.reshape(negative_batch, (1, 10, 8192))


# Network building
net = tflearn.input_data([None, width, height])
net = tflearn.lstm(net, 128*4, dropout=0.5)
net = tflearn.fully_connected(net, classes, activation='softmax')
net = tflearn.regression(net, optimizer='adam', learning_rate=learning_rate, loss='categorical_crossentropy')
model = tflearn.DNN(net, tensorboard_verbose=0)

## add this "fix" for tensorflow version errors
for x in tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES): tf.add_to_collection(tf.GraphKeys.VARIABLES, x )

# Training

while training_iters > 0:
	trainX, trainY = next(positive_batch)
	testX, testY = next(positive_batch)  # todo: proper ;)
	model.fit(trainX, trainY, n_epoch=2, validation_set=(testX, testY), show_metric=True, batch_size=batch_size)
	trainX, trainY = next(negative_batch)
	testX, testY = next(negative_batch)  # todo: proper ;)
	model.fit(trainX, trainY, n_epoch=2, validation_set=(testX, testY),  show_metric=True, batch_size=batch_size)
	training_iters -= 1
	print("THE CURRENT TRAINING ITER IS", training_iters)

model.save("tflearn.lstm.model")
_y = model.predict(next(positive_batch)[0])  # << add your own voice here
_z = model.predict(next(negative_batch)[0])  # << add your own voice here

print (_y)
print(_z)