# tranpose.py
"""
Transpose dialog window.

This file is part of the program
LeMMA - a GUI Frontend for creating MMA files.

Note that this is NOT really an MMA editor, but rather a simple front-end to MMA
Please read help.txt and CHANGES for more information.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Gek S. Low <geksiong@yahoo.com>

"""

from .GSTkWidgets import *
import re
import logging

NOTES = {
	'C': 0,
	'C#': 1, 'Db': 1,
	'D': 2,
	'D#': 3, 'Eb': 3,
	'E': 4,
	'F': 5,
	'F#': 6, 'Gb': 6,
	'G': 7,
	'G#': 8, 'Ab': 8,
	'A': 9,
	'A#': 10, 'Bb': 10,
	'B': 11,
	}

BASE_LETTERS = "CDEFGAB"

LETTERS = {
	'C': 0,
	'D': 1,
	'E': 2,
	'F': 3,
	'G': 4,
	'A': 5,
	'B': 6,
	}

SHARP_KEYS = ('C','C#','D','D#','E','F','F#','G','G#','A','A#','B')
FLAT_KEYS = ('C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B')

def isValidKeySig(key):
	p = re.compile('^([A-G])([#b]{0,1})(\s*(m|min|maj|minor|major){0,1})$')
	m = p.match(key)
	if m != None:
		base = m.group(1)
		acc = m.group(2)
		suffix = m.group(3)
		if base+acc in ['Cb','E#','Fb','B#']:	# MMA seems to accept these keys though
			logging.debug("[isValidKeySig] Invalid current key: "+key)
			return False
	else:
		logging.debug("[isValidKeySig] Invalid current key: "+key)
		return False
	return True

# Transpose a note from currentKey to newKey
# Returns new note if no errors found
# otherwise returns the original note (i.e. no transpose)

def transposeNote(note, currentKey, newKey, dbl_acc=True):
	#print "Transpose", note, "from", currentKey, "to", newKey, "is",

	sharpKey = True

	# Determine note number
	# need to account for double accidentals here!
	pNote = re.compile('^([A-G])([#b]{0,2})')
	mNote = pNote.match(note)
	if mNote != None:
		baseNote = mNote.group(1)
		accNote = mNote.group(2)
	else:
		logging.debug("[transposeNote] Invalid note: " + note)
		return note
	noteNum = NOTES[baseNote]
	for ch in accNote:
		if ch == '#':
			noteNum += 1
		if ch == 'b':
			noteNum -= 1
	#print "Note Number: ", noteNum

	# Get base keys and major/minor
	p = re.compile('^([A-G])([#b]{0,1})(\s*(m|min|maj|minor|major){0,1})$')
	m1 = p.match(currentKey)
	if m1 != None:
		base1 = m1.group(1)
		acc1 = m1.group(2)
		suffix1 = m1.group(3)
		if base1+acc1 in ['Cb','E#','Fb','B#']:
			logging.debug("[transposeNote] Invalid current key: "+currentKey)
			return note	# don't transpose if invalid key
	else:
		logging.debug("[transposeNote] Invalid current key: "+currentKey)
		return note	# don't transpose if invalid key

	m2 = p.match(newKey)
	if m2 != None:
		base2 = m2.group(1)
		acc2 = m2.group(2)
		suffix2 = m2.group(3)
		if acc2 == 'b':
			sharpKey = False
		if base2+acc2 in ['Cb','E#','Fb','B#']:
			logging.debug("[transposeNote] Invalid new key: "+newKey)
			return note	# don't transpose if invalid key
	else:
		logging.debug("[transposeNote] Invalid new key: "+newKey)
		return note	# don't transpose if invalid key

	# don't want to support transpose between major/minor at this moment
	if suffix1 != suffix2:
		logging.debug("[transposeNote] Major/Minor doesn't match!")
		return note	# don't transpose if incompatible keys

	baseOffset = LETTERS[base2] - LETTERS[base1]
	actualOffset = NOTES[base2+acc2] - NOTES[base1+acc1]

	#print "Letter: ", baseOffset
	#print "Actual: ", actualOffset

	# Determine new base letter
	newNoteBase = ""
	newNoteBase = BASE_LETTERS[(LETTERS[baseNote] + baseOffset) % 7]
	#print newNoteBase

	# Adjust accidentals
	newActualNote = ""
	if sharpKey:
		newActualNote = SHARP_KEYS[(noteNum + actualOffset) % 12]
	else:
		newActualNote = FLAT_KEYS[(noteNum + actualOffset) % 12]
	#print newActualNote

	adjust = NOTES[newActualNote] - NOTES[newNoteBase]
	if adjust < -2:
		adjust += 12
	elif adjust > 2:
		adjust -= 12
	#print adjust
	newNote = newNoteBase
	if adjust == -1:
		newNote += 'b'
	elif adjust == -2:
		if dbl_acc == True:
			newNote += 'bb'
		else:
			newNote = newActualNote
	elif adjust == 1:
		newNote += '#'
	elif adjust == 2:
		if dbl_acc == True:
			newNote += '##'
		else:
			newNote = newActualNote
	elif adjust != 0:
		print('unexpected adjust value: ' , adjust)
	#print newNote
	return newNote


# Parse a line and transposes the notes
def transposeLine(line, currentKey, newKey, dbl_acc=True):
	def transposeMatch(match, currentKey=currentKey, newKey=newKey, dbl_acc=dbl_acc):
		return transposeNote(match.group(), currentKey, newKey, dbl_acc)

	pNote = re.compile('([A-G][#b]{0,2})')
	newLine = pNote.sub(transposeMatch,line)
	#print newLine
	return newLine

class TransposeDialog(SimpleDialogExt):
	def __init__(self, master=None, currentKey="C"):
		self.currentKey = currentKey
		self.newKey = ""
		self.selectedKey = StringVar()

		invalidKey = False
		p = re.compile('^([A-G][#b]{0,1})(\s*(m|min|maj|minor|major){0,1})$')
		m = p.match(currentKey)
		if m != None:
			self.keyBase = m.group(1)
			self.keySuffix = m.group(2)
			if self.keyBase in ['Cb','E#','Fb','B#']:
				invalidKey = True
		else:
			invalidKey = True

		if not invalidKey:
			SimpleDialogExt.__init__(self, master, title="Transpose song")
		else:
			tkinter.messagebox.showinfo("Invalid Key Signature", "Please use a valid key signature")

	def body(self, master):
		Label(master=master, text="Select a key signature").grid(row=0, column=0, sticky=NW)
		note_num = NOTES[self.keyBase]

		self.frame = Frame(master=master)
		self.frame.grid(row=1, column=0, sticky=EW)

		for index in range(12):
			if SHARP_KEYS[index] == FLAT_KEYS[index]:
				Radiobutton(master=self.frame, text=SHARP_KEYS[index] + self.keySuffix, variable=self.selectedKey, value=SHARP_KEYS[index] + self.keySuffix, indicatoron=False, width=15, padx=5, pady=5).grid(row=index, column=0, columnspan=2, sticky=EW)
			else:
				Radiobutton(master=self.frame, text=SHARP_KEYS[index] + self.keySuffix, variable=self.selectedKey, value=SHARP_KEYS[index] + self.keySuffix, indicatoron=False, width=15, padx=5, pady=5).grid(row=index, column=0, sticky=EW)
				Radiobutton(master=self.frame, text=FLAT_KEYS[index] + self.keySuffix, variable=self.selectedKey, value=FLAT_KEYS[index] + self.keySuffix, indicatoron=False, width=15, padx=5, pady=5).grid(row=index, column=1, sticky=EW)
		self.selectedKey.set(self.currentKey)

	def apply(self):
		self.newKey = self.selectedKey.get()
		return

# Testing

def main():
	transposeNote("D", "C", "Eb")
	transposeNote("B", "Am", "Em")
	transposeNote("C", "Dm", "Ebm")
	transposeNote("A#", "C", "G")
	transposeNote("Ab", "Bb", "Eb")
	transposeNote("E#", "C", "C#")
	transposeNote("E#", "C", "C#", dbl_acc = False)
	transposeNote("C", "B", "C")
	transposeLine("Cmaj7 Dm E7 F6 G", "B", "C")

if __name__ == "__main__":
	main()
