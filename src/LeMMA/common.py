# common.py
"""
Common functions

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

# Common
from GSTkWidgets import *
import os
import re
import subprocess
import cPickle
import commands
import platform
import ConfigParser

from constants import *
import constants
import logging
import fonts

try:
	import pygame
	pygame.init()
	pygame.mixer.init()
	pygame.mixer.music.set_volume(1.0)
	hasPyGame = True
except:
	hasPyGame = False

# Global variables
isLinux = None
mmaPath = ""
midiEngine = ""
midiPlayer = ""
pythonPath = ""
customGroovePath = ""

initialMeasuresPerRow = 4
MeasuresPerRow = initialMeasuresPerRow

groovesFile = ""
settingsFile = ""

libDir = ""

playerIsPaused = True

outputWindow = Text()

def detectPlatform():
	global isLinux
	# Assume Linux platform is default if not Windows
	# The subprocess calls under Windows are handled a bit differently
	if platform.system() not in ("Windows", "Microsoft"):
		isLinux = True
	else:
		isLinux = False
	logging.debug("[detectPlatform] isLinux = " + str(isLinux) + ", platform.system() returns '" + platform.system() + "'")

	# Debug log: check if pygame was successfully imported
	if hasPyGame:
		logging.debug("[detectPlatform] PyGame was loaded")
	else:
		logging.debug("[detectPlatform] PyGame not loaded")


def printOutput(text, append=False):
	if append == False:
		outputWindow.delete("1.0", END)
		outputWindow.insert("1.0", text + "\n")
	else:
		outputWindow.insert(END, text + "\n")
	outputWindow.update()

def autoDetectPaths():
	global pythonPath
	global mmaPath

	# Python path
	pythonPath = sys.executable
	if pythonPath != "":
		printOutput("Found python at " + pythonPath, True)
		logging.debug("[AutoDetectPaths] Found python at " + pythonPath)
	else:
		printOutput("Unable to find python!", True)
		logging.debug("[AutoDetectPaths] Found python at " + pythonPath)

	# MMA path
	if os.path.exists('/usr/local/bin/mma'):
		mmaPath = '/usr/local/bin/mma'
		printOutput("Found MMA at " + mmaPath, True)
		logging.debug("[AutoDetectPaths] Found MMA at " + mmaPath)
	elif os.path.exists('/usr/bin/mma'):
		mmaPath = '/usr/bin/mma'
		printOutput("Found MMA at " + mmaPath, True)
		logging.debug("[AutoDetectPaths] Found MMA at " + mmaPath)
	elif os.path.exists('C:\mma\mma.py'):
		mmaPath = 'C:\mma\mma.py'
		printOutput("Found MMA at " + mmaPath, True)
		logging.debug("[AutoDetectPaths] Found MMA at " + mmaPath)
	elif os.path.exists(os.path.normpath(os.getcwd() + '/mma.py')):
		mmaPath = os.path.normpath(os.getcwd() + '/mma.py')
		printOutput("Found MMA at " + mmaPath, True)
		logging.debug("[AutoDetectPaths] Found MMA at " + mmaPath)
	else:
		printOutput("Unable to auto-detect MMA path. Please set it manually in 'Settings'", True)
		logging.debug("[AutoDetectPaths] Unable to auto-detect MMA path")

	# MMA grooves path
	determineLibDir()


def determineLibDir():
	# try different locations for the libraries
	# try the lib directory from mma path first
	global libDir
	global mmaPath
	mmaDir = os.path.dirname(mmaPath)

	if os.path.exists("/usr/local/share/mma/lib"):
		libDir = "/usr/local/share/mma/lib"
		printOutput("Grooves directory is " + libDir, True)
		logging.debug("[determineLibDir] Found " + libDir + " when MMA path is " + mmaPath)
	elif os.path.exists("/usr/share/mma/lib"):
		libDir = "/usr/share/mma/lib"
		printOutput("Grooves directory is " + libDir, True)
		logging.debug("[determineLibDir] Found " + libDir + " when MMA path is " + mmaPath)
	elif os.path.exists(os.path.normpath(mmaDir + "/lib")):
		libDir = os.path.normpath(mmaDir + "/lib")
		printOutput("Grooves directory is " + libDir, True)
		logging.debug("[determineLibDir] Found " + libDir + " when MMA path is " + mmaPath)
	else:
		#libDir = "";
		printOutput("Couldn't find the Grooves directory. Perhaps your MMA path is incorrect?", True)
		logging.debug("[determineLibDir] Unable to determine when MMA path is " + mmaPath)
		return

def setConfigPath(configPath):
	global settingsFile
	global groovesFile

	settingsFile = os.path.normpath(configPath + "/settings.dat")
	groovesFile = os.path.normpath(configPath + "/grooves.dat")


def readSettings():
	global mmaPath
	global midiEngine
	global midiPlayer
	global pythonPath
	global customGroovePath
	global libDir
	global settingsFile
	global initialMeasuresPerRow
	global MeasuresPerRow
	
	# load settings (if file exists)
	try:
		config = ConfigParser.ConfigParser()
		config.read(settingsFile)

		pythonPath = config.get("paths", "python")
		mmaPath = config.get("paths", "mma")
		midiPlayer = config.get("paths", "midiplayer")
		libDir = config.get("paths", "grooves")
		customGroovePath = config.get("paths", "customgrooves")
		try:
			m = int(config.get("misc", "measures_per_row"))
			initialMeasuresPerRow = m
			MeasuresPerRow = m
		except:
			logging.debug("[readSettings] Measures per row not an integer! Using default of " + str(MeasuresPerRow))
		midiEngine = config.get("misc", "midiengine")
	except:
		printOutput("Error opening " + settingsFile + ". Will try to auto-detect. Please check settings later.", True)
		logging.debug("[readSettings] Cannot find " + settingsFile)
		autoDetectPaths()


def playMMA():
	global mmaPath

	# validate the paths first
	if not os.path.exists(mmaPath):
		tkMessageBox.showerror("Error", "MMA Path: '" + mmaPath + "' does not exist. Please check your settings.")
		return
	if os.path.isdir(pythonPath):
		tkMessageBox.showerror("Error", "Python path: '" + pythonPath + "' is a directory and not a filename. Please check your settings.")
		return
	if os.path.isdir(mmaPath):
		tkMessageBox.showerror("Error", "MMA path: '" + mmaPath + "' is a directory and not a filename. Please check your settings.")
		return


	# run MMA - must run from mma.py path
	currentdir = os.getcwd()
	mmaDir = os.path.dirname(mmaPath)
	os.chdir(mmaDir)
	
	tempmidifile = os.path.normcase(currentdir + "/_temp_.mid")
	# delete the temp midi file first, if any
	try:
		os.remove(tempmidifile)
		logging.debug("[playMMA] Temp midi " + tempmidifile + " deleted.")
	except:
		logging.debug("[playMMA] No temp midi to delete.")

	# Generate the midi file
	cmd = os.path.normcase(pythonPath + " " + mmaPath + " \"" + currentdir + "/_temp_.mma\"")
	logging.debug("[playMMA] Calling process '" + cmd + "'")
	pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).stdout
	output = pipe.read()
	status = pipe.close()

	os.chdir(currentdir)
	
	#print output
	printOutput(output)

	# Check temp midi file exists, return if not found
	if not os.path.exists(tempmidifile):
		tkMessageBox.showerror("Error", "Failed to generate midi from MMA.")
		logging.debug("[playMMA] Temp midi not created. Nothing to play.")
		return

	# Choose the midi engine to play the file
	if midiEngine == "PyGame":
		playMMA_pygame(tempmidifile)
	else:
		playMMA_external(tempmidifile)
	
def playMMA_external(filename):
	global midiPlayer

	realmidipath = re.compile(r'\s-[^\s]*').sub("", midiPlayer)	# strip any command-line options
	if not os.path.exists(realmidipath):
		tkMessageBox.showerror("Error", "Midi player: '" + midiPlayer + "' does not exist. Please check your settings.")
		#return		# non-fatal error in case of bugs

	# play Midi
	if isLinux == False:
		# On windows, need shell=False to avoid a shell window
		useShell = False
	else:
		# On Linux, need shell=True for this to work, but note that there is no way to control/stop timidity.
		useShell = True

	# On windows, can't use os.popen as that will wait for process to finish, then I'll have to close the midi player all the time
	midiopts = midiPlayer.replace(realmidipath, "")	# get any command-line options in midiPlayer
	cmd = os.path.normcase("\"" + realmidipath + "\" " + midiopts + " \"" + filename + "\"")
	logging.debug("[playMMA] Calling process '" + cmd + "'")
	pipe = subprocess.Popen(cmd, shell=useShell, stdout=None).stdout


def playMMA_pygame(filename):
	global hasPyGame
	global playerIsPaused

	if not hasPyGame:
		tkMessageBox.showerror("Error", "PyGame not found! Please use another midi engine.")
	else:
		if playerIsPaused:
			pygame.mixer.music.unpause()
			playerIsPaused = False
		else:
			pygame.mixer.music.load(filename)
			pygame.mixer.music.play()


def stop_playMMA():
	global hasPyGame
	global playerIsPaused

	if midiEngine == "PyGame":
		if not hasPyGame:
			tkMessageBox.showerror("Error", "PyGame not found! Please use another midi engine.")
		else:
			pygame.mixer.music.stop()
			playerIsPaused = False
	else:
		tkMessageBox.showinfo("Not available", "Stop playback is available only for PyGame midi engine.")

def pause_playMMA():
	global hasPyGame
	global playerIsPaused

	if midiEngine == "PyGame":
		if not hasPyGame:
			tkMessageBox.showerror("Error", "PyGame not found! Please use another midi engine.")
		else:
			# only need to pause if still playing music
			if pygame.mixer.music.get_busy():
				pygame.mixer.music.pause()
				playerIsPaused = True
	else:
		tkMessageBox.showinfo("Not available", "Pause playback is available only for PyGame midi engine.")

class ViewFileDialog(SimpleDialogExt):
	contents = ""

	def __init__(self, parent, title=None, filename="", linenumbers=False):
		self.linenumbers=linenumbers
		try:
			f = open(filename, "r")
			self.contents = f.read()
			f.close()
		except:
			printOutput("Can't open "+filename)
			return
		SimpleDialogExt.__init__(self, parent, title, text1="Close", text3="")

	def body(self, master):
		self.viewText = Text(master, width=50, height=20, bg="white", wrap=WORD, font=autoScaleFont(FONTS["Text"]))
		if self.linenumbers:
			(font, size, style) = self.viewText["font"].split(" ")
			tabwidth = str(4 * int(size))
			self.viewText.tag_configure("linenum", {'background': '#e0e0e0', 'tabs': tabwidth, 'font': ('Courier',size,style) })
			self.viewText.tag_configure("normal", {'lmargin1': '0', 'lmargin2': tabwidth})

			# Add line numbers if true
			#new_contents = ""
			i = 1
			lines = self.contents.split("\n")
			for line in lines:
				self.viewText.insert(INSERT, str(i) + "\t", "linenum")
				self.viewText.insert(INSERT, line + "\n", "normal")
				i += 1
			#self.contents = new_contents
		else:
			self.viewText.insert("1.0", self.contents)
		self.viewText.configure(state=DISABLED)
		self.viewText.grid(row=0, column=0, sticky=N+S+E+W)

		self.viewScrollY = AutoScrollbar(master, orient=VERTICAL, command=self.viewText.yview)
		self.viewScrollY.grid(row=0, column=1, stick=NS)
		self.viewText["yscrollcommand"] = self.viewScrollY.set

		self.viewScrollX = AutoScrollbar(master, orient=HORIZONTAL, command=self.viewText.xview)
		self.viewScrollX.grid(row=1, column=0, stick=EW)
		self.viewText["xscrollcommand"] = self.viewScrollX.set
	
	def apply(self):
		return


class CodeDialog(SimpleDialogExt):
	code = ""
	def __init__(self, parent, code=""):
		self.code = code
		SimpleDialogExt.__init__(self, parent, title="Insert MMA commands", text1="Update")

	def body(self, master):
		self.codeText = Text(master, width=50, height=20, bg="white", wrap=NONE, font=autoScaleFont(FONTS["Text"]))
		self.codeText.insert("1.0", self.code)
		self.codeText.grid(row=0, column=0, sticky=N+S+E+W)

		self.codeScrollY = AutoScrollbar(master, orient=VERTICAL, command=self.codeText.yview)
		self.codeScrollY.grid(row=0, column=1, stick=NS)
		self.codeText["yscrollcommand"] = self.codeScrollY.set

		self.codeScrollX = AutoScrollbar(master, orient=HORIZONTAL, command=self.codeText.xview)
		self.codeScrollX.grid(row=1, column=0, stick=EW)
		self.codeText["xscrollcommand"] = self.codeScrollX.set
	
		return self.codeText
	
	def apply(self):
		self.code = self.codeText.get("1.0", END)
		return

	def buttonbox(self):
		SimpleDialogExt.buttonbox(self)
		# Need to remove the enter key binding as it conflicts with the text widget
		self.unbind("<Return>")
		return


