# settings.py
"""
Settings dialog window.

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

# Settings
from .GSTkWidgets import *
import os
import re
import subprocess
import pickle
import subprocess
import platform
import configparser

from .constants import *

import logging
from . import fonts
from . import common

# Global variables
groovedict = {}
groovelib_lookup = {} # given a groove name and libpath, look up the groove library
currentgroovelib = ""

def readGrooves():
	global groovedict
	global groovelib_lookup
	try:
		f = open(common.groovesFile, "r")
		p = pickle.Unpickler(f)
		groovedict = p.load()
		groovelib_lookup = p.load()
		f.close()
	except IOError:
		common.printOutput("Error opening " + common.groovesFile + ". Please check your settings, then refresh the grooves.", True)


class SettingsDialog(SimpleDialogExt):
	def __init__(self, parent, lemma_modulepath):
		self.modulePath = lemma_modulepath
		SimpleDialogExt.__init__(self, parent, title="Settings", text1="Save")

	def body(self, master):
		Label(master, text="Python path ", anchor=W).grid(row=0, column=0, sticky=W)
		self.pythonPathEntry = Entry(master, width=20, font=autoScaleFont(FONTS["Text"]))
		self.pythonPathEntry.insert(1, common.pythonPath)
		self.pythonPathEntry.grid(row=0, column=1, columnspan=3, sticky=E+W)
		self.browse_icon = default_icons.getIcon("folder-open")
		self.pythonPathBrowseBtn = Button(master, image=self.browse_icon, text="Browse", command=self.pythonPathBrowse)
		self.pythonPathBrowseBtn.grid(row=0, column=4, sticky=NW)
		
		Label(master, text="MMA path ", anchor=W).grid(row=1, column=0, sticky=W)
		self.mmaPathEntry = Entry(master, width=20, font=autoScaleFont(FONTS["Text"]))
		self.mmaPathEntry.insert(1, common.mmaPath)
		self.mmaPathEntry.grid(row=1, column=1, columnspan=3, sticky=E+W)
		self.mmaPathBrowseBtn = Button(master, image=self.browse_icon, text="Browse", command=self.mmaPathBrowse)
		self.mmaPathBrowseBtn.grid(row=1, column=4, sticky=NW)

		Label(master, text="MMA grooves path ", anchor=W).grid(row=2, column=0, sticky=W)
		self.mmaLibDirEntry = Entry(master, width=20, font=autoScaleFont(FONTS["Text"]))
		self.mmaLibDirEntry.insert(1, common.libDir)
		self.mmaLibDirEntry.grid(row=2, column=1, columnspan=3, sticky=E+W)
		self.mmaLibDirBrowseBtn = Button(master, image=self.browse_icon, text="Browse", command=self.mmaLibDirBrowse)
		self.mmaLibDirBrowseBtn.grid(row=2, column=4, sticky=NW)

		Label(master, text="Midi engine ", anchor=W).grid(row=3, column=0, sticky=W)
		self.midiEngineButton = Button(master, text=common.midiEngine, pady=0)
		self.midiEngineButton.grid(row=3, column=1, sticky=E+W)
		self.midiEngineComboMenu = ComboMenu(master, attachto=self.midiEngineButton, text=">")
		self.midiEngineComboMenu.setList(("External midi player", "PyGame"))
		self.midiEngineComboMenu.grid(row=3, column=2, sticky=NW)

		Label(master, text="External midi player ", anchor=W).grid(row=4, column=0, sticky=W)
		self.midiPlayerEntry = Entry(master, width=20, font=autoScaleFont(FONTS["Text"]))
		self.midiPlayerEntry.insert(1, common.midiPlayer)
		self.midiPlayerEntry.grid(row=4, column=1, columnspan=3, sticky=E+W)
		self.midiPlayerBrowseBtn = Button(master, image=self.browse_icon, text="Browse", command=self.midiPlayerBrowse)
		self.midiPlayerBrowseBtn.grid(row=4, column=4, sticky=NW)

		Label(master, text="(Optional) Custom \ngroove folder ", anchor=W, justify=LEFT).grid(row=5, column=0, sticky=W)
		self.customGroovePathEntry = Entry(master, width=20, font=autoScaleFont(FONTS["Text"]))
		self.customGroovePathEntry.insert(1, common.customGroovePath)
		self.customGroovePathEntry.grid(row=5, column=1, columnspan=3, sticky=E+W)
		self.customGroovePathBrowseBtn = Button(master, image=self.browse_icon, text="Browse", command=self.customGrooveBrowse)
		self.customGroovePathBrowseBtn.grid(row=5, column=4, sticky=NW)

		Label(master, text="Measures per row \n(on startup) ", anchor=W, justify=LEFT).grid(row=6, column=0, sticky=W)
		self.measuresPerRowEntry = Entry(master, width=3, font=autoScaleFont(FONTS["Text"]))
		self.measuresPerRowEntry.insert(1, common.initialMeasuresPerRow)
		self.measuresPerRowEntry.grid(row=6, column=1, sticky=W)

		Label(master, text="").grid(row=7, column=0)

		self.autoDetectBtn = Button(master, text="Auto-detect paths", command=self.autoDetectPaths)
		self.autoDetectBtn.grid(row=8, column=1, padx=7, sticky=E+W)

		self.mmaPathRefreshBtn = Button(master, text="Refresh grooves library", command=self.refreshGrooves)
		self.mmaPathRefreshBtn.grid(row=8, column=2, padx=7, sticky=E+W)

		self.configFontsBtn = Button(master, text="Configure fonts", command=self.configFonts)
		self.configFontsBtn.grid(row=8, column=3, padx=7, sticky=E+W)

		return self.mmaPathEntry	# initial focus
	
	def autoDetectPaths(self):
		if tkMessageBox.askokcancel("Warning", "Your current settings will be overwritten. Continue?"):
			common.autoDetectPaths()
			self.pythonPathEntry.delete(0, END)
			self.pythonPathEntry.insert(1, common.pythonPath)

			self.mmaPathEntry.delete(0, END)
			self.mmaPathEntry.insert(1, common.mmaPath)

			self.mmaLibDirEntry.delete(0, END)
			self.mmaLibDirEntry.insert(1, common.libDir)
	

	def mmaPathBrowse(self):
		currentFile = tkFileDialog.askopenfilename(parent=self)
		if currentFile != "" and currentFile != ():
			currentFile = os.path.normpath(currentFile)
			self.mmaPathEntry.delete(0, END)
			self.mmaPathEntry.insert(1, currentFile)

	def mmaLibDirBrowse(self):
		currentFile = tkFileDialog.askdirectory(parent=self)
		if currentFile != "" and currentFile != ():
			currentFile = os.path.dirname(os.path.normpath(currentFile)+"/") # dir name
			self.mmaLibDirEntry.delete(0, END)
			self.mmaLibDirEntry.insert(1, currentFile)

	def pythonPathBrowse(self):
		currentFile = tkFileDialog.askopenfilename(parent=self)
		if currentFile != "" and currentFile != ():
			currentFile = os.path.normpath(currentFile)
			self.pythonPathEntry.delete(0, END)
			self.pythonPathEntry.insert(1, currentFile)
	
	def midiPlayerBrowse(self):
		currentFile = tkFileDialog.askopenfilename(parent=self)
		if currentFile != "" and currentFile != ():
			currentFile = os.path.normpath(currentFile)
			self.midiPlayerEntry.delete(0, END)
			self.midiPlayerEntry.insert(1, currentFile)

	def customGrooveBrowse(self):
		currentFile = tkFileDialog.askdirectory(parent=self)
		if currentFile != "" and currentFile != ():
			currentFile = os.path.dirname(os.path.normpath(currentFile)+"/") # dir name
			self.customGroovePathEntry.delete(0, END)
			self.customGroovePathEntry.insert(1, currentFile)
	
	def apply(self):
		# read variables and strip trailing spaces	
		pythonPath = self.pythonPathEntry.get().strip(' ')
		mmaPath = self.mmaPathEntry.get().strip(' ')
		libDir = self.mmaLibDirEntry.get().strip(' ')
		midiEngine = self.midiEngineButton["text"]
		midiPlayer = self.midiPlayerEntry.get().strip(' ')
		customGroovePath = self.customGroovePathEntry.get().strip(' ')
		measuresPerRow = self.measuresPerRowEntry.get().strip(' ')

		logging.debug("[Settings] Settings are: (" + pythonPath + "," + mmaPath + "," + midiPlayer + "," + customGroovePath + ")")
		# validate the existence of these paths
		if not os.path.exists(pythonPath):
			tkMessageBox.showerror("Error", "Python path: '" + pythonPath + "' does not exist.")
			return
		if not os.path.exists(mmaPath):
			tkMessageBox.showerror("Error", "MMA path: '" + mmaPath + "' does not exist.")
		if os.path.isdir(pythonPath):
			tkMessageBox.showerror("Error", "Python path: '" + pythonPath + "' is a directory and not a filename.")
			return
		if os.path.isdir(mmaPath):
			tkMessageBox.showerror("Error", "MMA path: '" + mmaPath + "' is a directory and not a filename.")
			return

		if not os.path.exists(libDir):
			tkMessageBox.showerror("Error", "MMA grooves path: '" + libDir + "' does not exist.")
			return

		realmidipath = re.compile(r'\s-[^\s]*').sub("", midiPlayer)	# strip any command-line options
		if not os.path.exists(realmidipath):
			tkMessageBox.showwarning("Warning", "Midi player path: '" + midiPlayer + "' does not exist. You won't be able to play MMA files.")
		if os.path.isdir(realmidipath):
			tkMessageBox.showwarning("Warning", "Midi player path: '" + midiPlayer + "' is a directory and not a filename. You won't be able to play the MMA file.")

		if customGroovePath != "" and not os.path.exists(customGroovePath):
			tkMessageBox.showwarning("Warning", "Custom groove path: '" + customGroovePath + "' does not exist.")

		# save the settings into settings file

		config = configparser.ConfigParser()
		config.read(common.settingsFile)
		if not config.has_section("paths"):
			config.add_section("paths")
		config.set("paths", "python", pythonPath)
		config.set("paths", "mma", mmaPath)
		config.set("paths", "midiplayer", midiPlayer)
		config.set("paths", "grooves", libDir)
		config.set("paths", "customgrooves", customGroovePath)

		if not config.has_section("misc"):
			config.add_section("misc")
		config.set("misc", "measures_per_row", measuresPerRow)
		config.set("misc", "midiengine", midiEngine)

		f = open(common.settingsFile, "w")
		config.write(f)
		f.close()

		common.printOutput("Settings saved in " + common.settingsFile)

		# read the settings file to set the global variables
		common.readSettings()

	def configFonts(self):
		d = fonts.ConfigureGUI(self)

	def refreshGrooves(self):
		# get the latest paths from GUI
		mmaPath = self.mmaPathEntry.get().strip(' ')
		pythonPath = self.pythonPathEntry.get().strip(' ')
		customGroovePath = self.customGroovePathEntry.get().strip(' ')

		# validate paths
		if not os.path.exists(pythonPath):
			tkMessageBox.showerror("Error", "Python path: '" + pythonPath + "' does not exist. Please check your settings.")
			return
		if not os.path.exists(mmaPath):
			tkMessageBox.showerror("Error", "MMA path: '" + mmaPath + "' does not exist. Please check your settings.")
			return
		if os.path.isdir(pythonPath):
			tkMessageBox.showerror("Error", "Python path: '" + pythonPath + "' is a directory and not a filename. Please check your settings.")
			return
		if os.path.isdir(mmaPath):
			tkMessageBox.showerror("Error", "MMA path: '" + mmaPath + "' is a directory and not a filename. Please check your settings.")
			return

		if customGroovePath != "" and not os.path.exists(customGroovePath):
			tkMessageBox.showwarning("Warning", "Custom groove path: '" + customGroovePath + "' does not exist. These will not be added.")

		mmaDir = os.path.dirname(mmaPath)
		#mmaDir = re.compile(r'.*[\\/]').match(mmaPath).group()
		if common.libDir == "" or not os.path.exists(common.libDir):
			common.printOutput("Couldn't find the MMA grooves directory. Please check your settings.")
			return

		# clear out the grooves
		global groovedict
		global groovelib_lookup

		groovedict = {}
		groovelib_lookup = {}

		self.addGrooves(common.libDir, pythonPath, mmaPath)
		if customGroovePath != "":
			self.addGrooves(customGroovePath, pythonPath, mmaPath)
		#print groovedict
		#write groovedict to grooves file
		f = open(common.groovesFile, "w")
		p = pickle.Pickler(f)
		p.dump(groovedict)
		p.dump(groovelib_lookup)
		f.close()


	def addGrooves(self, currlibDir, pythonPath, mmaPath):
		# get all groove files starting from currlibDir, note this takes a while to complete
		mmaDir = os.path.dirname(mmaPath)
		#mmaDir = re.compile(r'.*[\\/]').match(mmaPath).group()

		currentdir = os.getcwd()
		os.chdir(mmaDir)
		
		global groovedict

		groovecount = 0
		p1 = re.compile(r'\\filehead\{(.*?)\}\{(.*?)\}')
		p2 = re.compile(r'\\instable\{(.*?)\}\{(.*?)\}')
		
		# check MMA version
		mmaversion = 1.2
		versionstr = ""
		try:
			#	quote pythonPath to handle correctly space characters in it
			cmd = "\"" + pythonPath + "\" " + mmaPath + " -v"
			#pipe = os.popen(cmd, 'r')
			pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).stdout
			output = pipe.read()
			versionstr = re.compile(r'^\d+\.\d+', re.S|re.M).search(output).group(0)
			mmaversion = float(versionstr)
			status = pipe.close()
			common.printOutput("Detected MMA version " + versionstr)
			logging.debug("[addGrooves] Detected MMA version " + versionstr)
		except:
			common.printOutput("Couldn't get MMA version! '" + cmd + "' Assuming version > 1.0")
			logging.debug("[addGrooves] Unable to get MMA version. Using '" + cmd + "'")

		# set the path part of the key to groovedict and groovelib_lookup
		# we'll define it as "<default>" if currlibDir matches the current global libDir
		# with this definition, currently loaded files will be less affected if libDir changes (when refreshing grooves)
		if currlibDir == common.libDir:
			keylibDir = "<default>"
		else:
			keylibDir = currlibDir

		# Count how many files we will be processing
		tree = os.walk(currlibDir)
		totalfiles = 0
		for directory in tree:
			for file in directory[2]:
				if file.endswith("mma"):
					totalfiles += 1
		#print totalfiles
		progressWin = ProgressBarWindow(self)

		filecount = 0.0
		tree = os.walk(currlibDir)
		# start walking the directory
		for directory in tree:
			for file in sorted(directory[2]):
				if file.endswith("mma"):
					filecount += 1.0
					filename = os.path.normcase(directory[0] + "/" + file)
					# run MMA command
					try:
						# NOTE: In Windows, I need a shell window for this to work!
						#	quote pythonPath to handle correctly space characters in it
						if mmaversion > 1.0:
							cmd = "\"" + pythonPath + "\" " + mmaPath + " -Dxl -w " + filename
						else:
							cmd = "\"" + pythonPath + "\" " + mmaPath + " -Dx -w " + filename
						pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE).stdout
						logging.debug("[addGrooves] Calling subprocess '" + cmd + "'")
						#pipe = os.popen(cmd, 'r')
						grooveinfo = pipe.read()
						status = pipe.close()
						
						#print grooveinfo
					except:
						#common.printOutput("Oops, an error was encountered")
						logging.debug("[addGrooves] Error encountered trying to run '" + cmd + "'")
						
					m1 = p1.search(grooveinfo)

					if m1 == None:
						continue

					groovelibname = m1.group(1)
					groovelibrary = groovelibname + "|" + keylibDir

					# Rename the groovelibrary if clashes found (the mambo grooves). This is no conflict as long as the grooves themselves don't clash. If so, it will depend on MMA's resolution rules.
					# Unfortunately, it happens that the yamaha grooves conflict with each other...
					if groovelibrary in list(groovedict.keys()):
						new_groovelibname = groovelibname
						libname_suffix = 1
						while (new_groovelibname + "|" + keylibDir) in list(groovedict.keys()):
							new_groovelibname = groovelibname + "_" + str(libname_suffix)
						groovelibrary = new_groovelibname + "|" + keylibDir
						logging.debug("[addGrooves] " + groovelibname + " renamed to " + new_groovelibname)

					groovedict[groovelibrary] = [m1.group(2), filename]
					
					#print groovedict
					m2 = p2.findall(grooveinfo)
					grooves = []
					
					headerstr = "[MMA " + versionstr + "] Reading grooves from " + currlibDir + "...\n"
					outputstr = headerstr + "Library: " + groovelibname + "\n"
					
					for groove in m2:	
						groovename = groove[0]
						groovedesc = groove[1]
						
						groovename = groovename.replace("\\\\","\\")
						groovename = groovename.replace("\\&","&")
						groovename = groovename.replace("``","`")
						groovename = groovename.replace("\"\"","\"")
						groovename = groovename.replace("\'\'","\'")
						
						groovedesc = groovedesc.replace("\\\\","\\")
						groovedesc = groovedesc.replace("\\&","&")
						groovedesc = groovedesc.replace("``","`")
						groovedesc = groovedesc.replace("\"\"","\"")
						groovedesc = groovedesc.replace("\'\'","\'")
						
						#print groovename
						
						outputstr += groovename + " "
						groovecount += 1
						
						grooves += [[groovename, groovedesc]]
						groovelib_lookup[groovename.lower()+"|"+keylibDir] = groovelibname
					groovedict[groovelibrary] += [grooves]
					
					common.printOutput(outputstr)
					#print filecount / totalfiles
					progressWin.set(filecount / totalfiles)

		progressWin.destroy()
		os.chdir(currentdir)
		common.printOutput(headerstr + "Done: Read " + str(groovecount) + " grooves")
		#print groovelib_lookup
		

class GroovesDialog(SimpleDialogExt):
	selectedGroove = ""
	selectedGroove_lib = ""
	selectedGroove_libpath = ""
	selectedGroove_autolibpath = ""
	currentgroove = ""

	def __init__(self, parent, groove=""):
		self.currentgroove = groove
		SimpleDialogExt.__init__(self, parent, title="Select Groove", text1="Update", text2="Clear", command2=self.clear)


	def body(self, master):
		global groovedict
		global groovelib_lookup
		global currentgroovelib

		# If there are no grooves in the dictionary, display error message and return
		if groovedict == {}:
			self.label = Label(master, text="No grooves yet! Please check MMA path setting and refresh grooves.")
			self.label.grid(row=0, column=0, sticky=N+S+E+W)
			return

		logging.debug("[GroovesDialog] Current groove in measure is: " + self.currentgroove + " at " + currentgroovelib)
		
		# If there are grooves, proceed
		keylist = list(groovedict.keys())

		keylist.sort()
		if currentgroovelib == "":
			currentgroovelib = keylist[0]
		else:
			if currentgroovelib not in list(groovedict.keys()):
				logging.debug("[GroovesDialog] Current groove " + self.currentgroove + " at " + currentgroovelib + " is not found.")
				self.label = Label(master, text="Groove not found in grooves dictionary")
				self.label.grid(row=0, column=0, sticky=N+S+E+W)
				return

		[groovelibname, groovelibpath] = currentgroovelib.split("|")

		self.mb = Menubutton(master, text=groovelibname, direction=RIGHT, relief=RAISED, width=len(groovelibname), takefocus=1, highlightbackground="white")
		self.mb.grid(row=0, column=0, sticky=NW)
	
		# the groove library names go into a menu
		self.mb.menu = Menu(self.mb, tearoff=0)
		self.mb["menu"] = self.mb.menu

		# define several cascade menus, we'll sort by alphabet
		menus = {}
		menuitems = {}
		for ch in "#ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			menus[ch] = Menu(self.mb, tearoff=0)
			menuitems[ch] = 0
			self.mb.menu.add_cascade(menu=menus[ch], label=ch)
		
		for key in keylist:
			[groovelibname, groovelibpath] = key.split("|")
			#print groovelibname, groovelibpath

			def updateListBox(key=key):
				self.__updateListBox(key)
				self.mb["width"] = len(self.mb["text"])

			if key[0] in "0123456789":
				menus["#"].add_command(label=groovelibname, command=updateListBox)
				menuitems["#"] += 1
			elif key[0].upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
				menus[key[0].upper()].add_command(label=groovelibname, command=updateListBox)
				menuitems[key[0].upper()] += 1
			else:
				logging.debug("[GroovesDialog] " + groovelibname + " does not begin with alphanumeric character")
			#self.mb.menu.add_command(label=key, command=updateListBox)
		# disable the cascade menus which are empty
		index = 0
		for ch in "#ABCDEFGHIJKLMNOPQRSTUVWXYZ":
			if menuitems[ch] == 0:
				self.mb.menu.entryconfigure(index, state=DISABLED)
			index += 1

		# which refreshes a listbox (with description)
		self.label = Label(master, text="Description: "+groovedict[currentgroovelib][0], anchor=NW, justify=LEFT, pady=10, wraplength=100)
		self.label.grid(row=1, column=0, sticky=N+S+E+W)
		
		self.lb = Listbox(master, width=50, height=15)
		location = groovedict[currentgroovelib][1]
		grooves = groovedict[currentgroovelib][2]
		grooves.sort()
		i = 0
		for groove in grooves:
			self.lb.insert(END, groove[0] + ": " + groove[1])
			if self.currentgroove.lower() == groove[0].lower():
				self.lb.selection_set(END)
			i = i + 1

		self.lb.grid(row=2, column=0, sticky=N+S+E+W)

		self.yScroll = AutoScrollbar(master, orient=VERTICAL)
		self.yScroll.grid(row=2, column=1, sticky=N+S)

		self.xScroll = AutoScrollbar(master, orient=HORIZONTAL)
		self.xScroll.grid(row=3, column=0, sticky=E+W)

		self.lb["xscrollcommand"] = self.xScroll.set
		self.lb["yscrollcommand"] = self.yScroll.set
		self.xScroll["command"] = self.lb.xview
		self.yScroll["command"] = self.lb.yview

		[groovelibname, libPath] = currentgroovelib.split("|")

		if libPath == "<default>":
			libPath = common.libDir
		libFile = location.replace(os.path.normcase(libPath + "/"), "")

		self.libPathLabel = Label(master, text="Library Path: " + libPath, anchor=NW, justify=LEFT, pady=0, wraplength=100)
		self.libPathLabel.grid(row=4, column=0, sticky=N+S+E+W)

		self.libFileLabel = Label(master, text="Library File: " + libFile, anchor=NW, justify=LEFT, pady=0, wraplength=100)
		self.libFileLabel.grid(row=5, column=0, sticky=N+S+E+W)

		self.update_idletasks()
		self.label.configure(wraplength=self.lb.winfo_width())
		self.libPathLabel.configure(wraplength=self.lb.winfo_width())
		self.libFileLabel.configure(wraplength=self.lb.winfo_width())
		self.lb.configure(height=min(self.lb.size(), 15))

		if self.lb.curselection() != ():
			self.lb.yview(self.lb.curselection())

		self.lb.focus()
		
	def __updateListBox(self, key):
		global groovedict
		global currentgroovelib
		if key != currentgroovelib:
			self.lb.delete(0, END)
			location = groovedict[key][1]
			grooves = groovedict[key][2]
			grooves.sort()
			for groove in grooves:
				self.lb.insert(END, groove[0] + ": " + groove[1])
			currentgroovelib = key
			[groovelibname, groovelibpath] = currentgroovelib.split("|")
			self.mb.configure(text=groovelibname, width=len(groovelibname))

			self.label.configure(text="Description: "+groovedict[key][0])

			[groovelibname, libPath] = currentgroovelib.split("|")
			if libPath == "<default>":
				libPath = common.libDir

			libFile = location.replace(os.path.normcase(libPath + "/"), "")
			self.libPathLabel.configure(text="Library Path: " + libPath)
			self.libFileLabel.configure(text="Library File: " + libFile)
			
			self.update_idletasks()
			#self.lb.configure(width=50)
			self.lb.configure(height=min(self.lb.size(), 15))

	def clear(self):
		self.selectedGroove = "<<CLEAR>>"
		self.cancel()

	def apply(self):
		global groovedict

		# If no grooves, return nothing
		if groovedict == {}:
			selected = ""
			return

		# If ok, get listbox selection
		if self.lb.curselection() != ():
			# groove name is taken from listbox
			selected = self.lb.get(self.lb.curselection())
			self.selectedGroove = re.compile(r':.*').sub("", selected)

			# groove lib name
			[self.selectedGroove_lib, groovelibpath] = currentgroovelib.split("|")

			# determine libpath setting
			temp = self.libPathLabel["text"]
			temp = temp.replace("Library Path: ", "")
			self.selectedGroove_libpath = temp

			# determine the autolibpath setting
			temp = self.libFileLabel["text"]
			temp = temp.replace("Library File: ", "")
			temp = os.path.normcase(self.selectedGroove_libpath + "/" + temp)
			temp = os.path.dirname(temp)
			temp = temp.replace(os.path.normcase(common.libDir + "/"), "")
			if temp == self.selectedGroove_libpath:
				self.selectedGroove_autolibpath = "."
			else:
				self.selectedGroove_autolibpath = temp

			# set selected groove libpath to "<default>" if it matches libDir
			if self.selectedGroove_libpath == common.libDir:
				self.selectedGroove_libpath = "<default>"

