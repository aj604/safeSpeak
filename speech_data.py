import os
import re
import sys
import wave

import numpy
import numpy as np

from random import shuffle

CHUNK = 4096


def load_wav_file(name):
	f = wave.open(name, "rb")
	# print("loading %s"%name)
	chunk = []
	data0 = f.readframes(CHUNK)
	while data0:  # f.getnframes()
		# data=numpy.fromstring(data0, dtype='float32')
		# data = numpy.fromstring(data0, dtype='uint16')
		data = numpy.fromstring(data0, dtype='uint8')
		data = (data + 128) / 255.  # 0-1 for Better convergence
		# chunks.append(data)
		chunk.extend(data)
		data0 = f.readframes(CHUNK)
	# finally trim:
	chunk = chunk[0:CHUNK * 2]  # should be enough for now -> cut
	chunk.extend(numpy.zeros(CHUNK * 2 - len(chunk)))  # fill with padding 0's
	# print("%s loaded"%name)
	return chunk

def wave_batch_generator(batch_size, path, label): #speaker
	batch_waves = []
	labels = []
	# input_width=CHUNK*6 # wow, big!!
	files = os.listdir(path)
	while True:
		shuffle(files)
		print("loaded batch of %d files" % len(files))
		for wav in files:
			if not wav.endswith(".wav"):continue
			labels.append(label)
			chunk = load_wav_file(path+wav)
			batch_waves.append(chunk)
			# batch_waves.append(chunks[input_width])
			if len(batch_waves) >= batch_size:
				yield batch_waves, labels
				batch_waves = []  # Reset for next batch
				labels = []