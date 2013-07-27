#!/usr/bin/env python2

def scale(note, key):
  """
  Given a starting note and a key, creates a list of notes in the scale.
  """
  TONE = 2
  SEMITONE = 1
  
  keys = {
      "major": [TONE, TONE, SEMITONE, TONE, TONE, TONE], 
      "natural_minor": [TONE, SEMITONE, TONE, TONE, SEMITONE, TONE], 
      "minor_pent": [3, TONE, TONE, 3], 
      "major_pent": [TONE, TONE, 3, TONE]
    }

  notes = [n.split(" ") for n in open("notes", "r").read().strip().split("\n")]
  notes = {a[0]:int(a[-1]) for a in notes}
  
  if note in notes and key in keys:
    values = []
    values.append(notes[note])
    for interval in keys[key]:
      values.append(values[-1]+interval)
    return values
  else:
    return None

if __name__ == "__main__":
  import sys
  note = sys.argv[1]
  key = sys.argv[2]

  print scale(note, key)
