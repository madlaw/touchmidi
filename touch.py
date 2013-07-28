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
	"""

	"""
	import sys
	import midi
	from notes import scale
	import jack
	from subprocess import call

	j = jack.Client("r")

	device = sys.argv[1]
	mode = sys.argv[2]

	d = Device(device)
	midi = midi.MidiPlayer()

	j.connect("jack-keyboard:midi_out","calf:organ_midi_in")
	j.connect("a2j:Midi Through [14] (capture): Midi Through Port-0","jack-keyboard:midi_in")

	if mode == "perc":
		start = 36
		mapping = range(start, start+6)
	if mode == "instr":
		start = 24
		# mapping = [prox, L, D, R, U, C]
		note = sys.argv[3]
		key = sys.argv[4]
		s = scale(note, key)
		mapping = [n+start for n in s]


		mapping.insert(0,[n+start for n in [s[0],s[2],s[4]]])
	olds = [False]*6
	threshold = 40
	min_velocity = 10

	windows = [MaxWindow() for i in range(6)]
	try:
		for line in d:
			print j.get_ports()
			for element, window in zip(line, windows):
				window.update(element)

			line = [window.value-element for element, window in zip(line, windows)]
			line_bool = [int(element>threshold) for element in line]

			for i,(current,old) in enumerate(zip(line_bool,olds)):
				if current and not old:
					velocity = int(min_velocity+(line[i]-threshold)*3.0)
					if not i == 0:
						midi.noteOn(mapping[i], velocity=velocity)
					else:
						midi.chordOn(mapping[i], velocity=velocity)
				if mode == "instr":
					if not current and old:
						if not i == 0:
							midi.noteOff(mapping[i])
						else:
							midi.chordOff(mapping[i])
				if current:
					print i,
			olds = line_bool
			print
	except KeyboardInterrupt:
		d.serial.close()
		call("./stopjack.sh")
