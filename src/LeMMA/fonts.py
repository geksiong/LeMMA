# fonts.py
"""
Fonts settings dialog window.

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
import tkinter.tix
from . import settings
from . import common
from .constants import *

import configparser
import logging

def readFonts():
	# read config file and override default fonts in constants.py
	config = configparser.ConfigParser()
	config.read(common.settingsFile)
	for i in range(7):
		confkey = "font." + FONTKEYS[i]
		if config.has_option("gui", confkey):
			fontdata = config.get("gui", "font." + FONTKEYS[i]).split(",")
			FONTS[FONTKEYS[i]] = (fontdata[0], fontdata[1], fontdata[2])

	# Fonts used for "toggle" states
	FONTS["Groove None"] = (FONTS["Groove"][0], FONTS["Groove"][1], "normal")
	FONTS["Code None"] = (FONTS["Code"][0], FONTS["Code"][1], "normal")

	#print FONTS

class ConfigureGUI(SimpleDialogExt):
	def __init__(self, parent, font=""):
		self.selectedFont = font
		readFonts()
		SimpleDialogExt.__init__(self, parent, title="Configure Fonts", text1="Save")

	def body(self, master):
		self.fontBtn = []
		self.fontSizeEntry = []
		self.fontStyleBtn = []
		self.tempFonts = []
		for i in range(7):
			Label(master, text=FONTKEYS[i], anchor=W).grid(row=i, column=0, sticky=W)
			self.tempFonts.append(())
			self.tempFonts[i] = FONTS[FONTKEYS[i]]
			#print self.tempFonts[i]

			def chooseFont(index=i):
				d = SelectFontDialog(self, title="Select Font", initfont=self.tempFonts[index])
				if d.selectedFont != "" and d.selectedFont != ():
					self.tempFonts[index] = d.selectedFont
					self.fontBtn[index]["text"] = d.selectedFont[0] + " | " + d.selectedFont[1]
					self.fontBtn[index].configure(font=autoScaleFont(d.selectedFont))
				return

			btn_text = FONTS[FONTKEYS[i]][0] + " | " + FONTS[FONTKEYS[i]][1]
			self.fontBtn += [Button(master, text=btn_text, width=20, font=autoScaleFont((self.tempFonts[i][0], FONTS["Base"][1], self.tempFonts[i][2])), command=chooseFont)]
			self.fontBtn[i].grid(row=i, column=1, sticky=E+W)

	def apply(self):
		# update the fonts
		for i in range(7):
			FONTS[FONTKEYS[i]] = self.tempFonts[i]

		FONTS["Groove None"] = (FONTS["Groove"][0], FONTS["Groove"][1], "normal")
		FONTS["Code None"] = (FONTS["Code"][0], FONTS["Code"][1], "normal")

		# save to settings.dat
		config = configparser.ConfigParser()
		config.read(common.settingsFile)
		if not config.has_section("gui"):
			config.add_section("gui")
		for key in list(FONTS.keys()):
			config.set("gui", "font." + key, FONTS[key][0] + "," + FONTS[key][1] + "," + FONTS[key][2])
		f = open(common.settingsFile, 'w')
		config.write(f)
		f.close()

		common.printOutput("Font settings saved to " + common.settingsFile)
		# Show info for now. Next time can reconfigure all fonts live.
		tkinter.messagebox.showinfo("Please restart LeMMA", "The new font settings will only fully take effect when you restart LeMMA")
		return

