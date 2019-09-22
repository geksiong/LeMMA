# app.py
"""
Application module.

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


# app.py

from .GSTkWidgets import *
import re
import pickle

from . import settings
from . import common
from .constants import *

import os
import logging

from . import fonts
from . import transpose

title = "LeMMA - a GUI frontend for creating MMA files"
version = "Version 0.9 alpha release (22 Aug 2010)"
copyright1 = "Created by Gek S. Low. Released under the GPL."
copyright2 = "This application uses public domain icons from the Tango Desktop Project (http://tango.freedesktop.org)"
MMA_filetypes = (("MMA files", "*.mma"), ("All files","*.*"))

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

SHARP_KEYS = ('C','C#','D','D#','E','F','F#','G','G#','A','A#','B')
FLAT_KEYS = ('C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B')


class Application(Frame):
	def __init__(self, master=None, lemma_configpath="", lemma_modulepath=""):
		Frame.__init__(self, master)
		self.currentFile = ""
		self.updateTitle()
		common.detectPlatform()
		self.modulePath = lemma_modulepath

		# If Linux and installed in /usr or /usr/local, use ~/.lemma for config directory
		# otherwise, store settings in application folder
		if lemma_configpath == "":
			if self.modulePath in ("/usr/local/share/lemma", "/usr/share/lemma") and common.isLinux:
				self.configPath = os.path.expanduser("~/.lemma")
				# Create the directory if this is missing
				if not os.path.isdir(self.configPath):
					os.mkdir(self.configPath)
					logging.debug("[app] Creating directory " + self.configPath)
			else:
				self.configPath = os.path.abspath(sys.path[0])
		else:
			# user-defined config path
			self.configPath = os.path.abspath(lemma_configpath)
		logging.debug("[app] Settings will be stored in " + self.configPath)
		common.setConfigPath(self.configPath)
	
		common.readSettings()
		settings.readGrooves()
		fonts.readFonts()

		self.grid(sticky=N+S+E+W)
		self.option_add("*font", autoScaleFont(FONTS["Base"]))
		self.createWidgets()

	def updateTitle(self):
		global title
		if self.currentFile == "" or self.currentFile == ():
			self.master.title(title + " (No file loaded)")
		else:
			self.master.title(title + " (" + os.path.basename(self.currentFile) + ")")

	def createWidgets(self):
		# Make top-level window resizable
		top=self.winfo_toplevel()
		top.rowconfigure(0, weight=1)
		top.columnconfigure(0, weight=1)
		self.rowconfigure(2, weight=1)
		self.columnconfigure(0, weight=1)

		# Menu
		menuList = (
			('File', 0, '', (
				('New', 0, 'Ctrl+N', self.newFile),
				('Open', 0, 'Ctrl+O', self.loadMMA),
				('Save', 0, 'Ctrl+S', self.saveMMA),
				('Save as ...', 0, '', self.saveAsMMA),
				('Quit', 0, '', self.quit),
				)),
			('MMA', 0, '', (
				('Preview', 4, '', self.viewMMA),
				('Play', 0, '', self.playFile),
				)),
			('Configure', 1, '', (
				('Settings', 0, '', self.settings),
				('Show/Hide output window', 1, '', self.toggleOutputWindow),
				)),
			('Help', 0, '', (
				('User guide', 0, '', self.help),
				('About LeMMA', 0, '', self.about),
				)),
		)

		self.menubar = createMenuBar(top, menuList)
		top.config(menu=self.menubar)

		# Toolbar
		self.Toolbar = createToolbar(self, os.path.abspath(self.modulePath+"/LeMMA/images"),
			(('file-new', 'New MMA file', self.newFile),
			('file-open', 'Open MMA file', self.loadMMA),
			('file-save', 'Save MMA file', self.saveMMA),
			('file-preview', 'Preview MMA file', self.viewMMA),
			('', '', None),
			('play', 'Play MIDI', self.playFile),
			('pause','Pause MIDI', self.pausePlayback),
			('stop', 'Stop MIDI', self.stopPlayback),
			('', '', None),
			('transpose', 'Transpose', self.transpose),
			('', '', None),
			('settings-system', 'Configure', self.settings),
			('help', 'Help', self.help),
			))
		self.Toolbar.grid(row=0, column=0, sticky=NW)

		self.showOutputWindow = True

		# Time Signature, Key Signature, Tempo
		self.infoFrame = Frame(self)
		self.infoFrame.grid(row=1, column=0, sticky=NW, padx=5, pady=5)
		
		Label(self.infoFrame, text="Time Sig ").grid(row=0, column=0, sticky=W)
		self.timeSigEntry = Entry(self.infoFrame, width=4)
		self.timeSigEntry.insert(1,"4/4")
		self.timeSigEntry.grid(row=0, column=1, sticky=W)

		self.timeSigComboMenu = ComboMenu(self.infoFrame, attachto=self.timeSigEntry, text=">")
		self.timeSigComboMenu.setList(("1/4","2/4","3/4","4/4","3/8","6/8"))
		self.timeSigComboMenu.grid(row=0, column=2, sticky=W)
		
		Label(self.infoFrame, text="   Key ").grid(row=0, column=3, sticky=W)
		self.keyEntry = Entry(self.infoFrame, width=4)
		self.keyEntry.insert(1,"C")
		self.keyEntry.grid(row=0, column=4, sticky=W)
		
		Label(self.infoFrame, text="   Tempo ").grid(row=0, column=5, sticky=W)
		self.tempoEntry = Spinbox(self.infoFrame, width=4, from_="0", to="400", increment=1)
		#self.tempoEntry = Entry(self.infoFrame, width=4)
		self.tempoEntry.delete(0, END)
		self.tempoEntry.insert(0,"120")
		self.tempoEntry.grid(row=0, column=6, sticky=W)
		self.tempoTip = ToolTip(self.infoFrame, attachto=self.tempoEntry, text="Tempo in beats/minute")
		
		self.SwingMode = IntVar()
		self.SwingMode.set(1)
		self.swingCheckBtn = Checkbutton(self.infoFrame, text="Swing Mode", command=None, variable=self.SwingMode)
		self.swingCheckBtn.grid(row=0, column=7, sticky=W)

		Label(self.infoFrame, text="     Measures/row ").grid(row=0, column=8, sticky=W)
		self.rowEntry = Spinbox(self.infoFrame, width=4, from_="1", to="16", increment=1, command=self.changeMeasuresPerRow)
		#self.rowEntry = Entry(self.infoFrame, width=4)
		self.rowEntry.delete(0, END)
		self.rowEntry.insert(0, common.MeasuresPerRow)
		self.rowEntry.grid(row=0, column=9, sticky=W)

		# This is where the chords are entered
		self.mainCanvas = Canvas(self, background=MAINFRAME_COLOR_BG, highlightthickness=0)
		self.mainCanvas.grid(row=2, column=0, sticky=N+S+E+W, padx=5, pady=5)
		self.mainFrame = Frame(self.mainCanvas, background=MAINFRAME_COLOR_BG, borderwidth=0)
		#self.mainFrame.grid(row=2, column=0, sticky=NW, padx=5, pady=5)
		
		self.scrollY = AutoScrollbar(self, orient=VERTICAL, command=self.mainCanvas.yview, takefocus=0)
		self.scrollY.grid(row=2, column=1, stick=N+S)
		self.scrollX = AutoScrollbar(self, orient=HORIZONTAL, command=self.mainCanvas.xview, takefocus=0)
		self.scrollX.grid(row=3, column=0, sticky=E+W)

		self.mainCanvas["xscrollcommand"] = self.scrollX.set
		self.mainCanvas["yscrollcommand"] = self.scrollY.set
		self.scrollX["command"] = self.mainCanvas.xview
		self.scrollY["command"] = self.mainCanvas.yview

		self.barnumbers = []
		self.measures = []
		self.grooves = []
		self.grooves_lib = []
		# this is used for SetLibPath directive
		self.grooves_libpath = []
		# this is used for SetAutoLibPath directive
		self.grooves_autolibpath = []
		self.barlines = []
		self.codebtns = []
		self.codes = []
		# See constants.py for default settings. Adjust to taste.
		for c in range(MEASURES_TOTAL):
			x = c % common.MeasuresPerRow
			y = c // common.MeasuresPerRow
			self.measures += [Measure(self.mainFrame, id=c)]
			self.barnumbers += [Label(self.mainFrame, text=str(c+1), justify=RIGHT, background=BARNUM_COLOR_BG, foreground=BARNUM_COLOR_FG_INACTIVE, takefocus=0, font=autoScaleFont(FONTS["Measure number"]))]
			def setGroove(index=c):
				if self.grooves[index]["text"] != GROOVE_TEXT_NONE:
					key = self.grooves[index]["text"] + "|" + self.grooves_libpath[index]
					if key.lower() in list(settings.groovelib_lookup.keys()):
						# set this again in case grooves dictionary has been updated
						self.grooves_lib[index] = settings.groovelib_lookup[key.lower()]
						settings.currentgroovelib = self.grooves_lib[index] + "|" + self.grooves_libpath[index]
					else:
						tkinter.messagebox.showwarning("Warning", "Groove "+self.grooves[index]["text"]+" is not found in LeMMA groove database")
						print(self.grooves_lib[index])
						settings.currentgroovelib = ""

					d = settings.GroovesDialog(self, self.grooves[index]["text"])
				else:
					d = settings.GroovesDialog(self, "")

				if d.selectedGroove == "<<CLEAR>>":
					self.grooves[index].configure(text=GROOVE_TEXT_NONE, foreground=GROOVE_COLOR_FG_NONE, font=autoScaleFont(FONTS["Groove None"]))
					self.grooves_lib[index] = ""
					self.grooves_libpath[index] = ""
					self.grooves_autolibpath[index] = ""
					logging.debug("[setGroove] No groove selected")
				elif d.selectedGroove != "":
					self.grooves[index].configure(text=d.selectedGroove, foreground=GROOVE_COLOR_FG, font=autoScaleFont(FONTS["Groove"]))
					self.grooves_lib[index] = d.selectedGroove_lib
					self.grooves_libpath[index] = d.selectedGroove_libpath
					self.grooves_autolibpath[index] = d.selectedGroove_autolibpath
					logging.debug("[setGroove] Selected: " + d.selectedGroove + " " + d.selectedGroove_lib + " " + d.selectedGroove_libpath + " " + d.selectedGroove_autolibpath)

			self.grooves += [FlatButton(self.mainFrame, text=GROOVE_TEXT_NONE, foreground=GROOVE_COLOR_FG_NONE, background=GROOVE_COLOR_BG, activebackground=GROOVE_COLOR_BG_MOUSEENTER, anchor=W, justify=LEFT, relief=FLAT, takefocus=0, command=setGroove, font=autoScaleFont(FONTS["Groove None"]), padx=0, pady=0, borderwidth=0, highlightthickness=0)]
			self.grooves_lib += [""]
			self.grooves_libpath += [""]
			self.grooves_autolibpath += [""]

			def setCode(index=c):
				d = common.CodeDialog(self, code=self.codes[index])
				self.codes[index] = d.code.strip()
				if self.codes[index] != "":
					self.codebtns[index].configure(foreground=CODE_COLOR_BG, background=CODE_COLOR_FG, font=autoScaleFont(FONTS["Code"]))
				else:
					self.codebtns[index].configure(foreground=CODE_COLOR_FG_NONE, background=CODE_COLOR_BG, font=autoScaleFont(FONTS["Code None"]))

			self.codes += [""]
			self.codebtns += [FlatButton(self.mainFrame, text=CODE_TEXT, foreground=CODE_COLOR_FG_NONE, background=CODE_COLOR_BG, activebackground=CODE_COLOR_BG_MOUSEENTER, anchor=W, justify=LEFT, relief=FLAT, takefocus=0, command=setCode, font=autoScaleFont(FONTS["Code None"]), padx=0, pady=0, borderwidth=0, highlightthickness=0)]
					
			def toggleBarlines(index=c):
				barline = self.barlines[index]["text"]
				if barline == " | ":
					self.barlines[index].configure(text=" |:")
				elif barline == " |:":
					self.barlines[index].configure(text=":| ")
				elif barline == ":| ":
					self.barlines[index].configure(text=":|:")
				else:
					self.barlines[index].configure(text=" | ")
			self.barlines += [FlatButton(self.mainFrame, text=" | ", justify=CENTER, takefocus=0, background=BARLINE_COLOR_BG, foreground=BARLINE_COLOR_FG, activebackground=BARLINE_COLOR_BG_MOUSEENTER, anchor=CENTER, relief=FLAT, font=autoScaleFont(FONTS["Bar"]), padx=0, pady=0, borderwidth=0, command=toggleBarlines, highlightthickness=0)]

		self.layoutMeasures()

		# Focus on the first measure and set up the main canvas
		self.measures[0].contents.focus()
		self.mainWindow = self.mainCanvas.create_window(0, 0, window=self.mainFrame, anchor=NW)
		self.adjustCanvasScroll(self.measures[0])

		self.outputText = Text(self, width=70, height=5, bg="white", wrap=WORD, relief=GROOVE, takefocus=0, font=autoScaleFont(FONTS["Text"]))
		self.outputText.grid(row=4, column=0, sticky=S+W+E, columnspan=2)
		
		common.outputWindow = self.outputText
		self.clearCanvas()

	def adjustCanvasScroll(self, measure):
		# Adjusts the size of scrolling area
		self.mainFrame.update_idletasks()
		self.mainCanvas.configure(scrollregion=self.mainCanvas.bbox(ALL))
		# need to scroll to the current measure?
		# Y scroll
		y1 = measure.winfo_y() - self.grooves[0].winfo_height()
		y2 = measure.winfo_y() + measure.winfo_height()
		h = self.mainFrame.winfo_height()
		f1 = float(y1) / h
		f2 = float(y2) / h
		(s1, s2) = self.scrollY.get()
		#print f1, f2, self.scrollY.get()
		if f1 < s1:
			self.mainCanvas.yview_moveto(f1)
		if f2 > s2:
			self.mainCanvas.yview_moveto(f2)
		
		# X scroll
		x1 = measure.winfo_x() - self.barlines[0].winfo_width()
		x2 = measure.winfo_x() + max(measure.winfo_width(), self.grooves[measure.id].winfo_width() + self.codebtns[measure.id].winfo_width())
		w = self.mainFrame.winfo_width()
		f1 = float(x1) / w
		f2 = float(x2) / w
		(s1, s2) = self.scrollX.get()
		#print f1, f2, self.scrollY.get()
		if f1 < s1:
			self.mainCanvas.xview_moveto(f1)
		if f2 > s2:
			self.mainCanvas.xview_moveto(f2)

	def changeMeasuresPerRow(self):
		common.MeasuresPerRow = int(self.rowEntry.get())
		self.layoutMeasures()
		self.adjustCanvasScroll(self.measures[0])

	def layoutMeasures(self):
		if common.MeasuresPerRow == 0:
			return
		for c in range(MEASURES_TOTAL):
			x = c % common.MeasuresPerRow
			y = c // common.MeasuresPerRow

			self.barlines[c].grid(row=y*2+1, column=x*3, sticky=W)
			self.measures[c].grid(row=y*2+1, column=x*3+1, sticky=W, columnspan=2)
			self.barnumbers[c].grid(row=y*2, column=x*3)
			self.grooves[c].grid(row=y*2, column=x*3+1, sticky=W)
			self.codebtns[c].grid(row=y*2, column=x*3+2, sticky=E)


	def newFile(self, event=None):
		if tkinter.messagebox.askokcancel("Warning", "All contents will be lost! Continue?"):
			self.currentFile = ""
			self.clearCanvas()
			self.updateTitle()
			common.printOutput("New file selected")

	def clearCanvas(self):
		for c in range(MEASURES_TOTAL):
			self.measures[c].contents.delete(0, END)
			self.measures[c].contents.configure(width=DEFAULT_MEASURE_WIDTH)
			self.grooves[c].configure(text=GROOVE_TEXT_NONE, foreground=GROOVE_COLOR_FG_NONE, font=autoScaleFont(FONTS["Groove None"]))
			self.grooves_lib[c] = ""
			self.grooves_libpath[c] = ""
			self.grooves_autolibpath[c] = ""
			self.barlines[c].configure(foreground=BARLINE_COLOR_FG_INACTIVE)
			self.barlines[c].configure(text=" | ")
			self.codes[c] = ""
			self.codebtns[c].configure(foreground=CODE_COLOR_FG_NONE, background=CODE_COLOR_BG, font=autoScaleFont(FONTS["Code None"]))
			self.barnumbers[c].configure(foreground=BARNUM_COLOR_FG_INACTIVE)

		# Update the canvas scroll area
		self.adjustCanvasScroll(self.measures[0])


	def loadMMA(self, event=None, filename=""):
		currentLibPath = common.libDir
		currentAutoLibPath = "stdlib"

		global MMA_filetypes
		if filename == "":
			temp = tkinter.filedialog.askopenfilename(filetypes = MMA_filetypes)
		else:
			temp = filename

		if temp == "" or temp == ():
			return
		else:
			self.currentFile = temp
			self.updateTitle()
		
		self.clearCanvas()
		f = open(self.currentFile, "r")
		i = 0 # measure number
		
		measure = 0
		repeatending_count = 1
		clearcontents = 1
		reached_first_measure = False
		
		# read each line
		for line in f:
			line = line.rstrip()

			matched = False
			
			if reached_first_measure == False and re.compile(r'^\s*KeySig\s*', re.IGNORECASE).match(line):
				line = re.compile(r'^\s*KeySig\s*', re.IGNORECASE).sub("", line)
				self.keyEntry.delete(0, END)
				self.keyEntry.insert(0, line)
				continue
			
			if reached_first_measure == False and re.compile(r'^\s*TimeSig\s*', re.IGNORECASE).match(line):
				line = re.compile(r'^\s*TimeSig\s*', re.IGNORECASE).sub("", line)
				line = line.replace(" " , "/")
				self.timeSigEntry.delete(0, END)
				self.timeSigEntry.insert(0, line)
				continue
			
			if reached_first_measure == False and re.compile(r'^\s*Tempo\s*', re.IGNORECASE).match(line):
				line = re.compile(r'^\s*Tempo\s*', re.IGNORECASE).sub("", line)
				self.tempoEntry.delete(0, END)
				self.tempoEntry.insert(0, line)
				continue
			
			if reached_first_measure == False and re.compile(r'^\s*SwingMode\s*', re.IGNORECASE).match(line):
				line = re.compile(r'^\s*SwingMode\s*', re.IGNORECASE).sub("", line)
				if line == "On":
					self.SwingMode.set(1)
					#self.swingCheckBtn.select()
				else:
					self.SwingMode.set(0)
					#self.swingCheckBtn.deselect()
				continue

			if re.compile(r'^\s*SetLibPath\s*', re.IGNORECASE).match(line):
				if not reached_first_measure:
					reached_first_measure = True
				line = re.compile(r'^\s*SetLibPath\s*', re.IGNORECASE).sub("", line)
				currentLibPath = line
				if currentLibPath == common.libDir:
					self.grooves_libpath[measure] = "<default>"
				else:
					self.grooves_libpath[measure] = currentLibPath
				continue
	
			if re.compile(r'^\s*SetAutoLibPath\s*', re.IGNORECASE).match(line):
				if not reached_first_measure:
					reached_first_measure = True
				line = re.compile(r'^\s*SetAutoLibPath\s*', re.IGNORECASE).sub("", line)
				currentAutoLibPath = line
				self.grooves_autolibpath[measure] = currentAutoLibPath
				continue
			
			if re.compile(r'^\s*Groove\s*', re.IGNORECASE).match(line):
				if not reached_first_measure:
					reached_first_measure = True
				line = re.compile(r'^\s*Groove\s*', re.IGNORECASE).sub("", line)
				if (' ' in line) or ('$' in line):	# more than just a groove name, make this a code line instead
					logging.debug("[loadMMA] Found a programmatic groove line, moving to code section: '"+line+"'")
					self.codes[measure] += "Groove " + line + "\n"
					self.codebtns[measure].configure(foreground=CODE_COLOR_BG, background=CODE_COLOR_FG, font=autoScaleFont(FONTS["Code"]))
					continue

				self.grooves[measure].configure(text=line, foreground=GROOVE_COLOR_FG, font=autoScaleFont(FONTS["Groove"]))
				if self.grooves_libpath[measure] == "":
					if currentLibPath == common.libDir:
						self.grooves_libpath[measure] = "<default>"
					else:
						self.grooves_libpath[measure] = currentLibPath
				if self.grooves_autolibpath[measure] == "":
					self.grooves_autolibpath[measure] = currentAutoLibPath
				# lookup the library file that contains this groove
				key = line + "|" + self.grooves_libpath[measure]
				if key.lower() in list(settings.groovelib_lookup.keys()):
					self.grooves_lib[measure] = settings.groovelib_lookup[key.lower()]
				else:
					tkinter.messagebox.showwarning("Warning", "Groove '"+line+"' is not found in LeMMA groove database. You may want to refresh it under 'Settings'.")
				continue

			if clearcontents == 1:
				contents = ""
			
			# is this a repeat, repeatending?
			if line == "Repeat":
				#contents = "|: "
				contents = ""
				matched = True
				# Is this a repeatend + repeat?
				if self.barlines[measure]["text"] == ":| ":
					self.barlines[measure].configure(text=":|:")
				else:
					self.barlines[measure].configure(text=" |:")
				repeatending_count = 1
				clearcontents = 0

			if line == "RepeatEnding":
				contents = "[" + str(repeatending_count) + " "
				matched = True
				repeatending_count += 1
				clearcontents = 0
				
			# form the measure contents field
			if re.compile(r'\d+').match(line):
				line = re.compile(r'^\d+\s*').sub("", line)
				contents = contents + line
				matched = True
				clearcontents = 1
			
			# is this a repeat end? then need to retrieve and add to previous bar
			if line == "RepeatEnd":
				self.barlines[measure].configure(text=":| ")
				#measure = measure - 1
				#contents = self.measures[measure].contents.get()
				#self.measures[measure].contents.delete(0, END)
				#contents += " :|"
				clearcontents = 1
				matched = True
			
			# insert into measure
			if clearcontents == 1 and contents != "":
				self.measures[measure].contents.insert(0, contents)
				measure = measure + 1
				if measure > len(self.measures):
					break
				continue
			
			if line == "cut -1":
				break

			# Must be some MMA code
			if reached_first_measure and not matched:
				#print measure, line
				self.codes[measure] += line + "\n"
				self.codebtns[measure].configure(foreground=CODE_COLOR_BG, background=CODE_COLOR_FG, font=autoScaleFont(FONTS["Code"]))

		# Check and adjust the measure widths
		for measure in self.measures:
			measure.adjustWidth(adjustScroll=False)

		# Update the canvas scroll area
		self.measures[0].contents.focus()
		self.adjustCanvasScroll(self.measures[0])
		self.measures[0].validateMeasures()
		f.close()

		# reset any pause settings
		common.playerIsPaused = False
		common.printOutput("Loaded " + self.currentFile)

	def viewMMA(self, event=None):
		self.doSaveMMA("_temp_.mma")
		common.ViewFileDialog(self, title="View MMA", filename="_temp_.mma", linenumbers=True)
	
	def playFile(self, event=None):
		self.doSaveMMA("_temp_.mma")
		common.playMMA()

	def pausePlayback(self, event=None):
		common.pause_playMMA()

	def stopPlayback(self, event=None):
		common.stop_playMMA()
		
	def saveMMA(self, event=None):
		# KeRi: if we have aready a filename save it as that
		if self.currentFile == "" or self.currentFile == ():	#	KeRi
			self.askAndSaveMMA()
		else:													#	KeRi
			self.doSaveMMA(self.currentFile)					#	KeRi
			common.printOutput("Saved " + self.currentFile)		#	KeRi
			return												#	KeRi
		
	def saveAsMMA(self, event=None):
		self.askAndSaveMMA()
	def askAndSaveMMA(self):
		temp = tkinter.filedialog.asksaveasfilename(filetypes = MMA_filetypes)
		if temp != "" and temp != ():
			self.currentFile = temp
			self.updateTitle()
			self.doSaveMMA(self.currentFile)
			common.printOutput("Saved as " + self.currentFile)
			return
		common.printOutput("Save cancelled")
		
	def doSaveMMA(self, filename):
		currentLibPath = common.libDir
		currentAutoLibPath = "stdlib"

		f = open(filename, "w")
		i = 0	# measure number
		print("// MMA file generated by LeMMA version " + version + "\n", file=f)
		print("KeySig " + self.keyEntry.get(), file=f)
		print("TimeSig " + self.timeSigEntry.get().replace("/", " "), file=f)
		print("Tempo " + self.tempoEntry.get() + "\n", file=f)
		if self.SwingMode.get() == 1:
			print("SwingMode On\n", file=f)
		else:
			print("SwingMode Off\n", file=f)
			
		#swingmode?
		reRepeatEnding = re.compile(r'\[\d+')

		for measure in self.measures:
			groove = self.grooves[i]["text"]
			if self.grooves_libpath[i] == "<default>":
				groove_libpath = common.libDir
			else:
				groove_libpath = self.grooves_libpath[i]
				
			groove_autolibpath = self.grooves_autolibpath[i]
			
			# set default groove (Folk) if first measure is empty
			if i == 0 and groove == GROOVE_TEXT_NONE:
				groove = "Folk"
				groove_libpath = common.libDir
				groove_autolibpath = "stdlib"
		
			contents = measure.contents.get()
			
			isRepeat = 0
			isRepeatEnd = 0
			isRepeatEnding = 0
			
			# Legacy stuff, if user types the repeat signs directly into measure text
			if contents.find("|:") != -1:
				isRepeat = 1
				contents = contents.replace("|:","")
				
			if contents.find(":|") != -1:
				isRepeatEnd = 1
				contents = contents.replace(":|","")
				
			if reRepeatEnding.match(contents):
				isRepeatEnding = 1
				contents = reRepeatEnding.sub("", contents) # first repeat
			
			contents = contents.strip(' ')
			if contents != "":
				printRepeat = False
				if self.barlines[i]["text"] == ":| ":
					print("RepeatEnd", file=f)
				if self.barlines[i]["text"] == ":|:":
					print("RepeatEnd", file=f)
					printRepeat = True

				# insert MMA codes first, if any
				if self.codes[i] != "":
					print(self.codes[i], file=f)

				# then print the groove
				if groove != GROOVE_TEXT_NONE:
					if groove_libpath != currentLibPath:
						print("SetLibPath " + groove_libpath, file=f)
						currentLibPath = groove_libpath
					if groove_autolibpath != currentAutoLibPath:
						print("SetAutoLibPath " + groove_autolibpath, file=f)
						currentAutoLibPath = groove_autolibpath
					print("Groove " + groove, file=f)

				# now for the measure
				# new barline approach to repeats
				if printRepeat or self.barlines[i]["text"] == " |:":
					print("Repeat", file=f)

				if isRepeat == 1:
					print("Repeat", file=f)
				if isRepeatEnding == 1:
					print("RepeatEnding", file=f)
				
				print(str(i+1) + " " + contents, file=f)
				
				if isRepeatEnd == 1:
					print("RepeatEnd", file=f)
			else:
				# insert any MMA codes in last measure
				if self.codes[i] != "":
					print(self.codes[i], file=f)

				break	# stops at first empty measure, ignoring any other non-empty measures after it
			i = i+1

		# need to consider a song ending in a repeat: must check beyond last bar
		if self.barlines[i]["text"] == ":| ":
			print("RepeatEnd", file=f)

		print("cut -1", file=f)
		f.close()

	def toggleOutputWindow(self, event=None):
		self.showOutputWindow = not self.showOutputWindow
		if self.showOutputWindow:
			self.outputText.grid()
		else:
			self.outputText.grid_remove()


	def about(self, event=None):
		global title, version, copyright1, copyright2

		abouthtml="""<html>
<center><b>%(title)s</b><br/>
%(version)s<br/><br/>
%(copyright1)s<br/><br/>
<i>%(copyright2)s</i>
</center>
</html>
		""" % { 'title': title, 'version': version, 'copyright1': copyright1, 'copyright2': copyright2}
		d = AboutDialog(self, aboutlogo=os.path.normpath(self.modulePath + "/lemma48.gif"), abouthtml = abouthtml)


	def help(self, event=None):
		d = ViewHtmlDialog(self, title="Help", filename=os.path.normpath(self.modulePath + "/help.htm"), basefont=autoScaleFont(FONTS["Text"]))

	def settings(self, event=None):
		d = settings.SettingsDialog(self, self.modulePath)

	def transpose(self, event=None):
		currentKey = self.keyEntry.get()
		d = transpose.TransposeDialog(self, currentKey)
		if d.newKey != "":
			# Set the new Key signature?
			self.keyEntry.delete(0, END)
			self.keyEntry.insert(1, d.newKey)
			# Transpose the contents of each measure
			for measure in self.measures:
				# Find the chords
				line = measure.contents.get()
				if line != "":
					# Transpose
					newLine = transpose.transposeLine(line, currentKey, d.newKey, dbl_acc=False)
					logging.debug("[transpose] (" + currentKey + " => " + d.newKey + ") " + line + " => " + newLine)
					measure.contents.delete(0, END)
					measure.contents.insert(1, newLine)
			# reset any pause in playback
			common.playerIsPaused = False


class AboutDialog(SimpleDialogExt):
	def __init__(self, master=None, aboutlogo=None, abouthtml=None):
		self.aboutlogo = aboutlogo
		self.abouthtml = abouthtml
		SimpleDialogExt.__init__(self, master, title="About LeMMA", text1="Ok", text3="")

	def body(self, master):
		self.logo = PhotoImage(file=self.aboutlogo)
		Label(master=master, image=self.logo).grid(row=0, column=0, sticky=NW)
		self.parser = SimpleTkHtml(master, autoScaleFont(FONTS["Base"]))
		self.parser.feed(self.abouthtml)
		self.viewHtml = self.parser.text
		self.viewHtml.configure(relief=FLAT, background=self["background"], height=10, width=60, bd=0, state=DISABLED)
		self.viewHtml.grid(row=0, column=1, sticky=N+S+E+W)

		self.viewScrollY = AutoScrollbar(master, orient=VERTICAL, command=self.viewHtml.yview)
		self.viewScrollY.grid(row=0, column=2, stick=NS)
		self.viewHtml["yscrollcommand"] = self.viewScrollY.set


	def apply(self):
		return

class Measure(Frame):
	def __init__(self, master=None, id=0):
		self.id = id
		Frame.__init__(self, master, borderwidth=0, bg=MAINFRAME_COLOR_BG)
		self.grid()
		self.createWidgets()
	
	def createWidgets(self):
		self.measurewidth=DEFAULT_MEASURE_WIDTH
		self.contents = Entry(self, width=DEFAULT_MEASURE_WIDTH, background=MEASURE_COLOR_BG, foreground=MEASURE_COLOR_FG, borderwidth=0, highlightcolor=MEASURE_COLOR_BG_FOCUS, highlightthickness=0, relief=FLAT, font=autoScaleFont(FONTS["Measure"]), justify=LEFT)
		self.contents.grid(row=0,column=0)
			
		self.contents.bind("<FocusOut>", self.doFocusOut)
		self.contents.bind("<FocusIn>", self.doFocusIn)
		self.contents.bind("<Enter>", self.doEnter)
		self.contents.bind("<Leave>", self.doLeave)
		self.contents.bind("<Up>", self.doJumpPreviousRow)
		self.contents.bind("<Down>", self.doJumpNextRow)
		self.contents.bind("<Left>", self.doJumpPreviousMeasure)
		self.contents.bind("<Right>", self.doJumpNextMeasure)
		self.contents.bind("<Alt-g>", self.doInvokeGrooveBtn)
		self.contents.bind("<Alt-c>", self.doInvokeCodeBtn)

	def doInvokeGrooveBtn(self, event):
		masterFrame = self.master
		masterCanvas = masterFrame.master
		masterApp = masterCanvas.master

		masterApp.grooves[self.id].invoke()
		self.contents.focus()

	def doInvokeCodeBtn(self, event):
		masterFrame = self.master
		masterCanvas = masterFrame.master
		masterApp = masterCanvas.master

		masterApp.codebtns[self.id].invoke()
		self.contents.focus()


	def doJumpPreviousMeasure(self, event):
		masterFrame = self.master
		masterCanvas = masterFrame.master
		masterApp = masterCanvas.master

		if self.contents.index(INSERT) == self.contents.index(0):
			newid = (self.id - 1) % MEASURES_TOTAL
			masterApp.measures[newid].contents.focus()

	def doJumpNextMeasure(self, event):
		masterFrame = self.master
		masterCanvas = masterFrame.master
		masterApp = masterCanvas.master

		if self.contents.index(INSERT) == self.contents.index(END):
			newid = (self.id + 1) % MEASURES_TOTAL
			masterApp.measures[newid].contents.focus()


	def doJumpPreviousRow(self, event):
		masterFrame = self.master
		masterCanvas = masterFrame.master
		masterApp = masterCanvas.master

		newid = (self.id - common.MeasuresPerRow) % MEASURES_TOTAL
		masterApp.measures[newid].contents.focus()

	def doJumpNextRow(self, event):
		masterFrame = self.master
		masterCanvas = masterFrame.master
		masterApp = masterCanvas.master

		newid = (self.id + common.MeasuresPerRow) % MEASURES_TOTAL
		masterApp.measures[newid].contents.focus()


	def doEnter(self, event):
		self.contents.configure(highlightbackground=MEASURE_COLOR_HIGHLIGHT_MOUSEENTER)

	def doLeave(self, event):
		self.contents.configure(highlightbackground=MEASURE_COLOR_HIGHLIGHT)

	def doFocusIn(self, event):
		masterFrame = self.master
		masterCanvas = masterFrame.master
		masterApp = masterCanvas.master

		if int(masterApp.rowEntry.get()) != common.MeasuresPerRow:
			common.MeasuresPerRow = int(masterApp.rowEntry.get())
			masterApp.layoutMeasures()

		self.contents.configure(background=MEASURE_COLOR_BG_FOCUS, foreground=MEASURE_COLOR_FG)
		self.adjustCanvasScroll()
		# first barline
		if self.id == 0:
			masterApp.barlines[0].configure(foreground=BARLINE_COLOR_FG)


	def validateMeasures(self):
		# Validate all the measures, toggle bar numbers, barlines
		masterFrame = self.master
		masterCanvas = masterFrame.master
		masterApp = masterCanvas.master

		reachedEnd = False
		for measure in masterApp.measures:
			measure.validateContents()
			if masterApp.barlines[measure.id]["text"] == "|| ":
				masterApp.barlines[measure.id]["text"] = " | "

			if measure.contents.get() != "" and reachedEnd == False:
				masterApp.barnumbers[measure.id].configure(foreground=BARNUM_COLOR_FG)
				masterApp.barlines[measure.id].configure(foreground=BARLINE_COLOR_FG)
			else:
				if not reachedEnd:
					masterApp.barlines[measure.id].configure(foreground=BARLINE_COLOR_FG)
					if measure.id != 0 and masterApp.barlines[measure.id]["text"] == " | ":
						masterApp.barlines[measure.id]["text"] = "|| "
					reachedEnd = True
				else:
					masterApp.barnumbers[measure.id].configure(foreground=BARNUM_COLOR_FG_INACTIVE)
					masterApp.barlines[measure.id].configure(foreground=BARLINE_COLOR_FG_INACTIVE)

	def adjustCanvasScroll(self):
		# need to scroll the canvas?
		masterFrame = self.master
		masterCanvas = masterFrame.master
		masterApp = masterCanvas.master
		masterApp.adjustCanvasScroll(self)


	def doFocusOut(self, event):
		masterFrame = self.master
		masterCanvas = masterFrame.master
		masterApp = masterCanvas.master

		# set background back to white
		self.contents.configure(background=MEASURE_COLOR_BG)
		self.validateContents()
		self.adjustWidth()
		# Toggle bar number, barline as active/inactive
		self.validateMeasures()

	def adjustWidth(self, adjustScroll=True):
		masterFrame = self.master
		masterCanvas = masterFrame.master
		masterApp = masterCanvas.master

		# Adjust the width
		w = len(str(self.contents.get()))
		if w >= DEFAULT_MEASURE_WIDTH:
			self.contents.configure(width=w+2)
		else:
			self.contents.configure(width=DEFAULT_MEASURE_WIDTH)
		self.contents.index(1)
		if self.contents["width"] != self.measurewidth:
			self.measurewidth = w
			if adjustScroll:
				masterApp.adjustCanvasScroll(self)

	def validateContents(self):
		valid = True
		measuretext = self.contents.get()
		p = re.compile('^\[[0-9]+ ', re.IGNORECASE)
		measuretext = p.sub("", measuretext)

		chords = measuretext.split()
		numchords = len(chords)
		if numchords == 0:
			self.contents.configure(foreground=MEASURE_COLOR_FG)
			return

		logging.debug("[app] Validating " + str(numchords) + " chords in measure " + str(self.id) + ": '" + measuretext + "'")

		# Check the number of beats
		masterFrame = self.master
		masterCanvas = masterFrame.master
		masterApp = masterCanvas.master
		timeSig = masterApp.timeSigEntry.get()
		[numbeats, temp] = timeSig.split("/")
		if numbeats == "" or numchords > int(numbeats):
			logging.debug("[app] Too many chords for " + timeSig)
			valid = False

		if self.id == 0 and chords[0] == "/":
			logging.debug("[app] First chord in first measure must be set")
			valid = False

		if valid == True:
			for chord in chords:
				if chord == "/":
					logging.debug("[app] Skipping over '/'")
					continue
				else:
					# convert all &'s to b's
					chord = chord.replace('&', 'b')
					p = re.compile('([A-Gz][#b!]{0,1})(.*)')
					m = p.match(chord)
					if m != None:
						chordkey = m.group(1)
						chordtype = m.group(2)
						if chordtype in CHORDTYPES:
							logging.debug("[app] Chord " + chord + " ok")
						else:
							valid = False
							logging.debug("[app] Chord " + chord + " is invalid!")
						break
					else:
						valid = False
						logging.debug("[app] Chord " + chord + " is invalid!")
						break
		if valid == True:
			logging.debug("[app] Measure is valid")
		else:
			logging.debug("[app] Measure is invalid")

		if valid:
			self.contents.configure(foreground=MEASURE_COLOR_FG)
		else:
			self.contents.configure(foreground=MEASURE_COLOR_FG_ERROR)


