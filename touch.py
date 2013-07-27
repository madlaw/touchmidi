#!/usr/bin/env python2

import serial

class MaxWindow(object):
	count = 1800
	def __init__(self):
		self.data = [0]

	def update(self, value):
		self.data.append(value)
		self.data = self.data[-self.count:]

	@property
	def value(self):
		return max(self.data)

class Device(object):
	def __init__(self, port="/dev/ttyACM0"):
		self.serial = serial.Serial(port)

	def __iter__(self):
		while True:
			line = self.serial.readline().strip().split(" ")
			if not len(line) == 6:
				continue
			line = map(int, line)
			yield line

if __name__ == "__main__":
	import sys
	import midi
	from notes import scale

	device = sys.argv[1]
	mode = sys.argv[2]

	d = Device(device)
	midi = midi.MidiPlayer()
	start = 36
	if mode == "perc":
		mapping = range(start, start+6)
	if mode == "instr":
		# mapping = [prox, L, D, R, U, C]
		note = sys.argv[3]
		key = sys.argv[4]
		s = scale(note, key)
		mapping = [n+start for n in s]
	olds = [False]*6
	threshold = 40
	min_velocity = 10

	windows = [MaxWindow() for i in range(6)]
	for line in d:
		for element, window in zip(line, windows):
			window.update(element)

		line = [window.value-element for element, window in zip(line, windows)]
		line_bool = [int(element>threshold) for element in line]

		for i,(current,old) in enumerate(zip(line_bool,olds)):
			if current and not old:
				midi.noteOn(mapping[i], velocity=int(min_velocity+(line[i]-threshold)*3.0))

			if mode == "instr":
				if not current and old:
					midi.noteOff(mapping[i])

			if current:
				print i,
		olds = line_bool
		print
