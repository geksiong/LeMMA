#!/usr/bin/env python
"""
Script to install lemma
For use with LeMMA version 0.8 and above

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

import os
import sys
import platform
import shutil
import stat
import getopt

PREFIX = "/usr/local"
NOPROMPT = False
errors = 0
TESTMODE = False

def prompt():
	input=input("...Press [ENTER] to continue, anything else to terminate: ")
	if input:
		print("Terminated by user...")
		sys.exit(1)
	else:
		print()

# Check for command-line arguments

try:
	opts, args = getopt.getopt(sys.argv[1:], "h", ["prefix=", "help", "noprompt", "test"])
except getopt.GetoptError as err:
	# print help information and exit:
	print(str(err))
	print()

for o, a in opts:
	if o in ("--prefix"):
		if a != "":
			PREFIX = a.rstrip('/')
	if o in ("--noprompt"):
		NOPROMPT = True
	if o in ("--test"):
		TESTMODE = True
	if o in ("--help", "-h"):
		print("Usage: install.py [--prefix=... (default: /usr/local)] [--noprompt]")
		sys.exit()

# Set the paths
BINDIR = PREFIX + "/bin"
LIBDIR = PREFIX + "/share/lemma"

print("This script will install LeMMA in " + BINDIR + " and " + LIBDIR)

# Check Linux platform
if platform.system() in ("Windows", "Microsoft"):
	print("You are running Windows. This script is for Linux.")
	print("To install in Windows, just copy the files to a directory of your choice")
	sys.exit(1)

# Warn if not running as root user
user = os.getuid()

if user != 0:
	print("[Warning] You should run this script as root user. Continue anyway?")

if not NOPROMPT:
	prompt()

# Check if BINDIR exists (shouldn't need this, just in case...)
if not (os.path.exists(BINDIR) and os.path.isdir(BINDIR)):
	print("[Warning] Directory " + BINDIR + " does not exist. Should I proceed?")
	if not NOPROMPT:
		prompt()
	# Create the BINDIR
	print("Creating " + BINDIR)
	try:
		if not TESTMODE:
			os.makedirs(BINDIR)
	except:
		# No point continuing now...
		print("[Error] Unable to create " + BINDIR)
		sys.exit(1)

# Copy LeMMA binary
print("Copying lemma.py to " + BINDIR + "/lemma")
try:
	if not TESTMODE:
		shutil.copy("lemma.py", BINDIR + "/lemma")
		os.chmod(BINDIR + "/lemma", 0o755)
except:
	print("[Error] Unable to copy!")
	errors += 1

# Check if LIBDIR exists
if os.path.exists(LIBDIR) and os.path.isdir(LIBDIR):
	print("[Warning] Directory " + LIBDIR + " exist. Should I proceed?")
	if not NOPROMPT:
		prompt()
else:
	# Create the LIBDIR
	print("Creating " + LIBDIR)
	try:
		if not TESTMODE:
			os.makedirs(LIBDIR)
	except:
		print("[Warning] Unable to create " + LIBDIR)
		sys.exit(1)

# In case LIBDIR/LeMMA is missing
try:
	if not TESTMODE:
		os.makedirs(LIBDIR + "/LeMMA")
except:
	print()

# LeMMA files and modules
filelist = ["README", "CHANGES", "help.htm", "lemma48.gif", "LeMMA/__init__.py", "LeMMA/app.py", "LeMMA/settings.py", "LeMMA/constants.py", "LeMMA/common.py", "LeMMA/fonts.py", "LeMMA/GSTkWidgets.py", "LeMMA/transpose.py"]
for filename in filelist:
	try:
		print("Copying " + filename + " to " + LIBDIR + "/" + filename)
		if not TESTMODE:
			shutil.copy2(filename, LIBDIR + "/" + filename)
	except:
		print("[Error] Unable to copy!")
		errors += 1

# Directories copy (non-recursive)
# Note: checkinstall couldn't seem to pick up files copies using shutil.copytree so we are copying one by one
dirlist = ["LeMMA/images"]

for dir in dirlist:
	# check it is really a dir
	if not os.path.isdir(dir):
		print("[Error] " + dir + " is not a directory! Skipping...")
		continue

	# Need to create the directory first?
	if not os.path.exists(LIBDIR + "/" + dir):
		print("Creating directory " + LIBDIR + "/" + dir)
		if not TESTMODE:
			os.makedirs(LIBDIR + "/" + dir)

	# Copy files
	for filename in os.listdir(dir):
		if os.path.isdir(filename):	# non-recursive, skip if directory
			continue

		src = dir + "/" + filename
		dest = LIBDIR + "/" + src
		print("Copying " + src + " to " + dest)
		try:
			if not TESTMODE:
				shutil.copy2(src, dest)
		except:
			print("[Error] Unable to copy!")

if errors > 0:
	print("\nErrors encountered during installation.")
else:
	print("\nInstallation complete.")

print("\nIf you want to uninstall LeMMA, just delete the file " + BINDIR + "/lemma and the directory " + LIBDIR + "\n")

print("Type \"lemma\" to run.")

