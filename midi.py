#!/usr/bin/env python2

import rtmidi

class MidiPlayer:
	def __init__(self):
		self.midiout = rtmidi.RtMidiOut()
		self.midiout.openPort(0)

	def noteOn(self, note, velocity=64):
		self.midiout.sendMessage(rtmidi.MidiMessage.noteOn(2L, 1, note, velocity))

	def noteOff(self, note):
		self.midiout.sendMessage(rtmidi.MidiMessage.noteOff(1, note))

if __name__ == "__main__":
	midi = MidiPlayer()


