#!/usr/bin/env python

"""
This file is part of the program
LeMMA - a GUI Frontend for creating MMA files.

Note that LeMMA is NOT really an MMA editor, but rather a simple front-end to MMA
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

import getopt
import logging
import os
import sys

modulepath = ""

# Where to look for LeMMA modules
for d in (os.path.abspath(os.path.dirname(__file__)), "/usr/local/share/lemma", "/usr/share/lemma"):
	if os.path.isdir(d) and d not in ("/usr/bin", "/usr/local/bin"):
		#print d
		sys.path.insert(0, d)
		modulepath = d
		break

from LeMMA.app import *
from LeMMA.settings import *

def printHelp():
	print(title)
	print(version)
	print(copyright1)
	print("""
Usage: lemma(.py) [options] [MMA file]

Command-line options:
	--help		This help message
	--debug		Turns on debug mode (run this from a shell window)
	--config=dir	Use "dir" for configuration settings
	""")

def main():
	loglevel = logging.ERROR
	configpath = ""

	# Look for any command-line options
	try:
		opts, args = getopt.getopt(sys.argv[1:], "h", ["debug", "config=", "help"])
	except getopt.GetoptError as err:
		# print help information and exit:
		print(str(err))
		print()
	for o, a in opts:
		if o in ("--debug"):
			loglevel = logging.DEBUG
		if o in ("--config"):
			configpath = a
		if o in ("--help", "-h"):
			printHelp()
			sys.exit()

	logging.basicConfig(level=loglevel, format="%(levelname)s:%(module)s:%(lineno)d:%(message)s")
	logging.debug("[main] LeMMA " + version + " - debug mode activated")
	logging.debug("[main] Module path found at " + modulepath)
	if configpath != "":
		logging.debug("[main] User-defined config path: " + configpath)

	# any file to load?
	filename = ""
	if args != []:
		filename = os.path.normpath(args[0])
		if os.path.exists(filename) and not os.path.isdir(filename):
			logging.debug("Filename provided at command-line: " + filename)
		else:
			logging.debug("Invalid filename provided at command-line: " + filename)
			filename = ""

	# Main
	app = Application(lemma_configpath=configpath, lemma_modulepath=modulepath)
	if filename != "":
		app.currentfile = filename
		app.loadMMA(filename)
	app.mainloop()

if __name__ == "__main__":
	main()
