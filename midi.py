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

	def chordOn(self, notes, velocity):
		for note in notes:
			self.noteOn(note, velocity)

	def chordOff(self, notes):
		for note in notes:
			self.noteOff(note)

if __name__ == "__main__":
	midi = MidiPlayer()


