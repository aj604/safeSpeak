import tensorflow as tf
import tflearn

import speech_data

from constants import positive_path, negative_path



learning_rate = 0.03
training_iters = 100  # steps
batch_size = 10

width = 20  # mfcc features
height = 80  # (max) length of utterance
classes = 1  # digits

positive_batch = word_batch = speech_data.wave_batch_generator(batch_size, positive_path, 1)
negative_batch = word_batch = speech_data.wave_batch_generator(batch_size, negative_path, 0)

# Network building
net = tflearn.input_data([None, width, height])
net = tflearn.lstm(net, 128*4, dropout=0.5)
net = tflearn.fully_connected(net, classes, activation='softmax')
net = tflearn.regression(net, optimizer='adam', learning_rate=learning_rate, loss='categorical_crossentropy')
model = tflearn.DNN(net, tensorboard_verbose=0)

## add this "fix" for tensorflow version errors
for x in tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES): tf.add_to_collection(tf.GraphKeys.VARIABLES, x )

# Training

while --training_iters > 0:
	trainX, trainY = next(positive_batch)
	testX, testY = next(positive_batch)  # todo: proper ;)
	model.fit(trainX, trainY, n_epoch=10, validation_set=(testX, testY), show_metric=True, batch_size=batch_size)
	trainX, trainY = next(negative_batch)
	testX, testY = next(negative_batch)  # todo: proper ;)
	model.fit(trainX, trainY, n_epoch=10, validation_set=(testX, testY), show_metric=True, batch_size=batch_size)

model.save("tflearn.lstm.model")
_y = model.predict(next(negative_batch)[0])  # << add your own voice here
print (_y)