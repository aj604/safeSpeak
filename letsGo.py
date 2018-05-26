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
classes = 2  # digits

positive_batch = word_batch = speech_data.wave_batch_generator(batch_size, POSITIVE_PATH, [1.0, 0.0])
negative_batch = word_batch = speech_data.wave_batch_generator(batch_size, NEGATIVE_PATH, [0.0, 1])
#positive_batch = np.reshape(positive_batch, (1, 10, 8192))
#negative_batch = np.reshape(negative_batch, (1, 10, 8192))


# Network building
'''net = tflearn.input_data(shape=[None, 8192])
net = tflearn.fully_connected(net, 64)
net = tflearn.dropout(net, 0.5)
net = tflearn.fully_connected(net, classes, activation='softmax')
net = tflearn.regression(net, optimizer='adam', loss='categorical_crossentropy')
'''

net = tflearn.input_data([None, width, height])
net = tflearn.lstm(net, 128*4, dropout=0.2)
net = tflearn.fully_connected(net, classes, activation='softmax')
net = tflearn.regression(net, optimizer='adam', learning_rate=learning_rate, loss='categorical_crossentropy')

model = tflearn.DNN(net, tensorboard_verbose=2)

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
print("Model Saved!")
print("Printing positive batch : ", positive_batch)
print("Printing positive batch with next: ", next(positive_batch))
#print("Printing len positive batch with next: ", next(positive_batch).shape)
print("Printing positive batch with next [0]: ", next(positive_batch)[0][0].shape)
print( model.predict(next(positive_batch)[0]))  # << add your own voice here

print("Printing negative batch")
_z = model.predict(next(negative_batch)[0])  # << add your own voice here

print(_z)