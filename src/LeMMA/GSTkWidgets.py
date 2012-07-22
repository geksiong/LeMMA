# GSTkWidgets.py
"""
GSTkWidgets - A hodge-podge collection of useful Tkinter widgets

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

from Tkinter import *
#from Tix import *
from Tkconstants import *

import tkFont
import tkSimpleDialog
import tkMessageBox
import tkFileDialog

# Used by SimpleTkHtml "widget"
from HTMLParser import HTMLParser
from Tkinter import *
import re
import os

# Used by IconSet
import binascii
import base64

def blah():
	tkMessageBox.showinfo("Under construction", "This feature is not yet implemented")

# Location of the icon images folder
icondir = os.path.abspath(os.path.dirname(__file__)+"/images")

# AutoScrollbar example taken from http://effbot.org/zone/tkinter-autoscrollbar.htm
class AutoScrollbar(Scrollbar):
	# a scrollbar that hides itself if it's not needed.  only
	# works if you use the grid geometry manager.
	def set(self, lo, hi):
		if float(lo) <= 0.0 and float(hi) >= 1.0:
			# grid_remove is currently missing from Tkinter!
			self.tk.call("grid", "remove", self)
		else:
			self.grid()
		Scrollbar.set(self, lo, hi)

	def pack(self, **kw):
		raise TclError, "cannot use pack with this widget"

	def place(self, **kw):
		raise TclError, "cannot use place with this widget"

# IconSet - manages a collection of icons. It dynamically loads the icons only when needed into memory.
# If iconid is invalid, it will try to load it as a filename
# A embedded missing icon image is returned if all attempts fail

class IconSet:
	def __init__(self, icondir="", iconlist={}):
		self.icondir = icondir	# root directory of icon images
		self.iconlist = iconlist	# map of icon ids and their corresponding image file locations
		self.iconmap = {}	# map of loaded icons in memory. icons are loaded on first lookup, and stay in the map thereafter.

		# define missing icon image

		# use commented code below to get base64 string for the icon
		#icon = PhotoImage(file=os.path.abspath(self.icondir+"/image-missing.gif"))
		#encoded=base64.b64encode(str(icon))
		#encoded=binascii.b2a_base64(icon)
		#encoded=base64.encodestring(open(os.path.abspath(self.icondir+"/image-missing.gif")).read())
		#print encoded

		# embedded 22x22 icon data
		self.missing_icon_data = '''
R0lGODlhFgAWAMZQAMwAAM0KCs4SEtAcG9AeHtEmJdMzMtQ4ONhVVYiKhdxzct6Af+COjeKdnOSu
rejEw9LS0tPT09TU1NXV1dPXz9PX0NbW1tfX19TZ0NbZ0tjY2NnZ2dfb09jb1Nra2urW1Nnc1tnd
1dvf2Nvf2d3g2t3h2uHh4d/i3eDi3OLi4uPj4+Lk3uLl3+Tk5OXl5eTm4ubm5ufn5+bo4+bo5Ojo
6Onp6ejq5ejq5urq6urr6Ovs6Ozu6u3u6u7u7O7w7e/w7fHx7/Hy7/Pz8/L08fP08vT19PX29Pb4
9vj49/n5+Pn7+vr7+vz8/Pz9/P7+//7//v//////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////
/////////////////////////////////////////////////////////////////////////yH5
BAEAAH8ALAAAAAAWABYAAAfQgH+Cg4SFhoMJiYqLjIqINFCRkpOUUEIJgglQEJwRERITExYXFxoa
Gx4eUJh/mpWvk6yaFLQUFRkdICMkKCsvMzY5q5lQFD3HyMnJPMOtxcrQyD/Ns8kAAA49BgLJQdRQ
GMkN1wwDCMlE3xzKDtcBC8lG3yHKDAbkyUjfIskLBAUf8B1T8q3EsQ8KDih4EI3JtxPRoj35xuKF
jBs6dvgAMqTIkSRLmjiJJAuWyW8mUqRQoaKFCxcwYsSgUaMGDhzUIJ2kRENWo5+NDgkdSrRoIAA7
'''
		self.missing_icon = None	# too early to create yet, as Tk hasn't been initialised. We'll create on the first getIcon call.


	def getIcon(self, iconid):
		# is it in the iconmap?
		if self.iconmap.has_key(iconid):
			return self.iconmap[iconid]
		else:
			# not loaded yet, check that it is in the defined list
			if self.iconlist.has_key(iconid):
				# get the icon from file and add it to the iconmap
				try:
					self.iconmap[iconid] = PhotoImage(file=os.path.abspath(self.icondir+"/"+self.iconlist[iconid]))
					return self.iconmap[iconid]
				except:
					# if missing, return a "missing image" icon
					if self.missing_icon == None:
						self.missing_icon = PhotoImage(data=self.missing_icon_data)
					return self.missing_icon
			else:
				# if it is not a valid iconid in the defined list, perhaps it is a filename?
				try:
					self.iconmap[iconid] = PhotoImage(file=os.path.abspath(self.icondir+"/"+iconid))
					return self.iconmap[iconid]
				except:
					# not a filename
					if self.missing_icon == None:
						self.missing_icon = PhotoImage(data=self.missing_icon_data)
					return self.missing_icon


default_icons = IconSet(icondir, {
	"combomenu-arrow": "combomenu_arrow.gif",
	"transpose": "transpose_btn.gif",
	"error": "dialog-error.gif",
	"info": "dialog-information.gif",
	"warn": "dialog-warning.gif",
	"file-new": "document-new.gif",
	"file-open": "document-open.gif",
	"file-print": "document-print.gif",
	"file-preview": "document-print-preview.gif",
	"file-properties": "document-properties.gif",
	"file-save-as": "document-save-as.gif",
	"file-save": "document-save.gif",
	"find": "edit-find.gif",
	"folder": "folder.gif",
	"folder-open": "folder-open.gif",
	"text-bold": "format-text-bold.gif",
	"text-italic": "format-text-italic.gif",
	"help": "help-browser.gif",
	"image-missing": "image-missing.gif",
	"add": "list-add.gif",
	"remove": "list-remove.gif",
	"eject": "media-eject.gif",
	"pause": "media-playback-pause.gif",
	"play": "media-playback-start.gif",
	"stop": "media-playback-stop.gif",
	"record": "media-record.gif",
	"seek-backward": "media-seek-backward.gif",
	"seek-forward": "media-seek-forward.gif",
	"skip-backward": "media-skip-backward.gif",
	"skip-forward": "media-skip-forward.gif",
	"settings-font": "preferences-desktop-font.gif",
	"settings-system": "preferences-system.gif",
	"fullscreen": "view-fullscreen.gif",
	"refresh": "view-refresh.gif",
	})


# Alternative flat button class - a Label that takes a command option
# Flat buttons are not supported on some platforms hence the need for this widget
# This is designed as a drop-in replacement for Button, but it does necessarily support all Button features

class FlatButton(Label):
	def __init__(self, master=None, cnf={}, **kw):
		# Identify and remove button-specific options
		# Only selected options are filtered
		self.options = {}
		self.fg = None
		self.bg = None
		self.enter = False

		if "command" in kw:
			self.options["command"] = kw["command"]
			del kw["command"]

		Label.__init__(self, master, cnf={}, **kw)

		# The below can only be done after initializing the widget
		# mouse bindings
		if "command" in self.options:
			self.bind("<Enter>", self.Enter)
			self.bind("<Leave>", self.Leave)
			self.bind("<ButtonRelease-1>", self.Release)


	def Enter(self, events):
		# Guard against entering again without leaving first (sometimes happen on Mac)
		if self.enter:
			return
		self.enter = True
		self["state"] = ACTIVE
		# The below is for Mac
		# get the latest fg and bg, as widget may have been reconfigured
		self.fg = self["fg"]
		self.bg = self["bg"]
		self["fg"] = self["activeforeground"]
		self["bg"] = self["activebackground"]

	def Leave(self, events):
		self.enter = False
		self["state"] = NORMAL
		# The below is for Mac
		self["fg"] = self.fg
		self["bg"] = self.bg

	def Release(self, events):
		if "command" in self.options:
			self.options["command"]()

	def invoke(self):
		self.Release(None)

# ToolTip - a Toplevel widget that is not meant to be grid/pack. It is initialised like a Label widget - the parameters are simply passed to the internal label.

class ToolTip(Toplevel):
	def __init__(self, master=None, attachto=None, **kw):
		Toplevel.__init__(self)
		#self.root = Toplevel()
		self.withdraw()
		self.overrideredirect(1)

		# This is necessary for it to work properly on Mac
		if self.tk.call("tk", "windowingsystem") == 'aqua':
			self.tk.call("::tk::unsupported::MacWindowStyle", "style", self._w, "help", "none")

		self.visible = False
		self.label = Label(self, background="#ffffe0", **kw)
		self.label.pack()

		self.attachto = attachto
		self.x = 0
		self.y = 0
		self.alarmid = 0

		# bind event to attachto
		if attachto:
			self.attachto.bind("<Enter>", self.startTip)
			self.attachto.bind("<Leave>", self.hideTip)
			self.attachto.bind("<Motion>", self.moveTip)

	def startTip(self, event):
		self.x = event.x_root + 20
		self.y = event.y_root + 20
		self.alarmid = self.attachto.after(500, self.showTip)

	def showTip(self):
		self.wm_geometry("+%d+%d" % (self.x, self.y))
		self.deiconify()
		self.visible = True

	def hideTip(self, event):
		self.withdraw()
		self.attachto.after_cancel(self.alarmid)
		self.visible = False

	def moveTip(self, event):
		self.x = event.x_root + 20
		self.y = event.y_root + 20
		if self.visible:
			self.wm_geometry("+%d+%d" % (self.x, self.y))

# A progress bar window

class ProgressBarWindow(Toplevel):
	def __init__(self, master=None, title="Please wait...", width=300, height=20, barcolor="#8eafd4", **kw):
		Toplevel.__init__(self, master)
		self.title(title)
		self.transient(master=master)
		#self.overrideredirect(1)
		self.resizable(width=False, height=False)
		self.protocol("WM_DELETE_WINDOW", self.close)

		# This is necessary for it to work properly on Mac
		if self.tk.call("tk", "windowingsystem") == 'aqua':
			self.tk.call("::tk::unsupported::MacWindowStyle", "style", self._w, "floating", "none")

		self.canvas = Canvas(self, width=width, height=height, border=2)
		self.canvas.pack()
		self.bar = self.canvas.create_rectangle(0,0,0,height, fill=barcolor)
		self.text = self.canvas.create_text(width/2, height/2, text='')
		self.value = 0.0

	def set(self, value=0.0, text=None):
		self.value = value
		if text == None:
			textstr = str(int(round(value * 100))) + " %"
			self.canvas.itemconfigure(self.text, text=textstr)
		else:
			self.canvas.itemconfigure(self.text, text=text)
		self.canvas.coords(self.bar, 0, 0, self.canvas.winfo_width()*value, self.canvas.winfo_height())
		self.canvas.update_idletasks()

	def close(self):
		# Do not allow window to be closed
		return


# Helper function to create top-level menubar from a list
"""
e.g. menulist = (('File', 0, 'Ctrl+F', (
			('New', 0, 'Ctrl+N', newfile),
			('Open', None, '', openFile),
		)))

"""
def createMenuBar(root, menu_list):
	def createSubMenu(root, parent, menuitem_list):
		menu = Menu(parent, tearoff=0)
		for menuitem in menuitem_list:
			name = menuitem[0]
			underline = menuitem[1]
			accelerator = menuitem[2]
			submenu_list = menuitem[3]
			if type(submenu_list) in (tuple, list):
				submenu = createSubMenu(root, menu, submenu_list)
				menu.add_cascade(label=name, menu=submenu, underline=underline, accelerator=accelerator)
			else:
				menu.add_command(label=name, command=submenu_list, underline=underline, accelerator=accelerator)

				# create an event binding for the accelerator
				if accelerator != "" and submenu_list != None:
					# translate some common accelerator styles
					event = accelerator.lower()
					event = event.replace("ctrl", "Control")
					event = event.replace("shift", "Shift")
					event = event.replace("alt", "Alt")
					event = event.replace("^", "Control-")
					event = event.replace("+", "-")
					#print event
					root.bind("<"+event+">", submenu_list)
		return menu

	menubar = createSubMenu(root, root, menu_list)
	return menubar

# ToolbarButton - Button with an embedded tooltip
# Can take either an image filename, or an iconid from the default icon set
# If iconid is given, it overrides the image filename param

class ToolbarButton(Button):
	def __init__(self, master=None, iconid=None, image="", tip="", command=None, *kw):
		self.image = None
		if iconid != "" and iconid != None:
			self.image = default_icons.getIcon(iconid)

		Button.__init__(self, master, image=self.image, command=command, *kw)
		self.tooltip = ToolTip(master, attachto=self, text=tip)


# Helper function to create a toolbar from a list
# Uses ToolTip widget to auto-generate tooltips
# Supports GIF images only
# Can accept either filenames or iconids from the default icon set
"""
e.g. toolbar_list = (('openfile.gif', 'Open a file', openfile),
		('savefile.gif', 'Saves a file', savefile),
		)
"""

def createToolbar(master, image_dir, toolbar_list):
	frame = Frame(master)
	for item in toolbar_list:
		imgres = item[0]
		tip = item[1]
		cmd = item[2]
		if imgres != "":
			# Create the button
			toolbutton = ToolbarButton(frame, iconid=imgres, tip=tip, command=cmd)
		else:
			# Separator
			toolbutton = Label(frame, text=" ")
		toolbutton.pack(side=LEFT)

	return frame

# Combomenu - a button that displays a scrolling listbox when clicked on, attaches itself to an Entry, Label or another Button

class ComboMenu(Button):
	def __init__(self, master=None, attachto=None, **kw):
		global icondir
		global default_icons
		self.arrow = default_icons.getIcon("combomenu-arrow")
		Button.__init__(self, master, command=self.showMenu, image=self.arrow, **kw)

		# create the popup menu, which is a listbox
		self.root = Toplevel()
		self.root.withdraw()

		# This is necessary for it to work properly on Mac
		# I used the 'modal' style but this is still not ideal. I can't dismiss the window 100% of the time by clicking outside, but you can click on the listbox and scrollbar so it's the most ideal I managed to find.
		# If you know of a better way please let me know.
		if self.root.tk.call("tk", "windowingsystem") == 'aqua':
			self.root.tk.call("::tk::unsupported::MacWindowStyle", "style", self.root._w, "modal", "none")

		self.listbox = Listbox(self.root, relief=FLAT)
		self.scroll = AutoScrollbar(self.root, orient='v', command=self.listbox.yview)
		self.listbox.configure(yscrollcommand=self.scroll.set)
		self.listbox.grid(row=0, column=0, sticky=E+W)
		self.scroll.grid(row=0, column=1, sticky=N+S)
		# The focus doesn't seem to work on Mac platform
		self.listbox.focus()

		# event bindings
		self.listbox.bind("<ButtonRelease-1>", self.updateEntry)
		self.listbox.bind("<Return>", self.updateEntry)
		self.listbox.bind("<Escape>", self.updateEntry)

		# attached widget
		self.attachto = attachto
		#print self.attachto.winfo_class()
		if self.attachto:
			# if entry widget
			if self.attachto.winfo_class() in ("Entry", "TEntry"):
				self.attachto.bind("<Down>", self.showMenu)
				self.attachto.bind("<Return>", self.showMenu)
			elif self.attachto.winfo_class() in ("Label", "TLabel"):
				self.attachto.bind("<ButtonRelease-1>", self.showMenu)
			elif self.attachto.winfo_class() in ("Button", "TButton"):
				self.attachto.configure(command=self.showMenu)

			# set button height to the widget's height
			self.configure(height=self.attachto.winfo_reqheight(), pady=0, padx=0)

		# try to set the list select to the contents of the attached widget
		self.autoSelect()

	def _press(self, event):
		#print "Clicked", event.widget.winfo_class()
		if event.widget != self.scroll:
			x,y = self.winfo_pointerxy()
			window = self.winfo_containing(x,y)
			#print x,y, event.x, event.y
			if window is None or window.winfo_toplevel() != self.root:
				self.updateEntry()

	def setList(self, list):
		self.listbox.delete(0, END)
		for item in list:
			self.listbox.insert(END, item)

		# adjust listbox height f less than 10 rows
		if len(list) < 10:
			self.listbox.configure(height=len(list))

	def updateEntry(self, event=None):
		if self.attachto.winfo_class() in ("Entry", "TEntry"):
			self.attachto.delete(0, END)
			self.attachto.insert(0, self.listbox.get(self.listbox.curselection()))
		else:
			self.attachto.configure(text=self.listbox.get(self.listbox.curselection()))

		#print "Selected ", self.listbox.get(self.listbox.curselection())
		self.hideMenu()

	def autoSelect(self):
		if self.attachto.winfo_class() in ("Entry", "TEntry"):
			select_text = self.attachto.get()
		else:
			select_text = self.attachto["text"]

		# note: only works if comparing strings with strings
		itemlist = self.listbox.get(0, END)
		try:
			pos = itemlist.index(select_text)
			#print pos
			self.listbox.select_set(pos)
		except:
			self.listbox.select_set(0)

	def showMenu(self, event=None):
		#print "Show"
		if self.attachto == None:
			x = self.winfo_rootx()
			y = self.winfo_rooty() + self.winfo_height()
		else:
			x = self.attachto.winfo_rootx()
			y = self.attachto.winfo_rooty() + self.attachto.winfo_height()
		self.root.geometry('+%d+%d' % (x,y))

		try:
			self.listbox.see(self.listbox.curselection())
		except:
			self.autoSelect()
			#self.listbox.select_set(0)

		self.root.bind("<ButtonRelease-1>", self._press)
		self.root.overrideredirect(1)
		self.root.deiconify()
		self.listbox.focus()
		self.root.grab_set_global()


	def hideMenu(self, event=None):
		#print "Hide"
		self.root.overrideredirect(0)
		self.root.withdraw()
		self.root.unbind("<ButtonRelease-1>")
		self.root.grab_release()
		self.attachto.focus()

	def destroy(self):
		self.root.destroy()
		Button.destroy(self)

# SimpleDialogExt - an extended version of tkSimpleDialog.Dialog
# Behaves like tkSimpleDialog.Dialog if extended params are not used
# 3 customisable buttons - text and actions, active button can be customised
# The middle button (button 2) will not be displayed if text2=="", regardless of whether a command is set for it
# default=<button number>, 0 means no default button set

class SimpleDialogExt(tkSimpleDialog.Dialog):
	def __init__(self, parent, title=None, text1="OK", text2="", text3="Cancel", command1=None, command2=None, command3=None, default=1, bind_ret=1, bind_esc=3):
		self.default_btn = default
		self.bind_ret = bind_ret
		self.bind_esc = bind_esc

		self.btntext = ["","",""]
		self.btntext[0] = text1
		self.btntext[1] = text2
		self.btntext[2] = text3

		self.btncmd = [None, None, None]
		if command1:	# OK button
			self.btncmd[0] = command1
		else:
			self.btncmd[0] = self.ok

		self.btncmd[1] = command2	# new middle button

		if command3:	# Cancel button
			self.btncmd[2] = command3
		else:
			self.btncmd[2] = self.cancel

		tkSimpleDialog.Dialog.__init__(self, parent, title)

	# customisable buttonbox
	def buttonbox(self):
		box = Frame(self)
		for i in range(3):
			if self.btntext[i] != "":
				if self.default_btn == i+1:
					setdefault = ACTIVE
				else:
					setdefault = DISABLED

				w = Button(box, text=self.btntext[i], width=10, command=self.btncmd[i], default=setdefault)
				w.pack(side=LEFT, padx=5, pady=5)
		box.pack()

		self.bind("<Return>", self.btncmd[self.bind_ret-1])
		self.bind("<Escape>", self.btncmd[self.bind_esc-1])


# SimpleTkHtml - A very, very simple html "widget". It is actually a HTMLParser with a Text widget inside.
# Nesting is generally NOT SUPPORTED
# Tables, attributes, font tags, frames, forms, scripts (obviously), imagemaps, embedded objects, etc etc are NOT SUPPORTED (remember this is simple)
# Note that the parser is sensitive to proper closing of tags. Take note especially that <img> and <br> tags must be written as <img /> and <br />

class SimpleTkHtml(HTMLParser):
	def __init__(self, master=None, basefont=None):
		# Init variables
		# The base font is used to init the styles
		if basefont == None:
			DF = ("Times", "10", "normal") # default font
		else:
			DF = basefont
		self.STYLES = {
			'html':	{'font': DF},
			'a': 	{'foreground': "blue",
				'underline': 1,
				},
			'b': 	{'font': (DF[0], DF[1], "bold")},
			'i': 	{'font': (DF[0], DF[1], "italic")},
			'h2': 	{'font': (DF[0], str(int(DF[1])+2), "bold"),
				},
			'h1': 	{'font': (DF[0], str(int(DF[1])+4), "bold"),
				},
			'p':	{},
			'ul':	{'lmargin1': 10, 'lmargin2': 20,},
			'ol':	{'lmargin1': 10, 'lmargin2': 30,},
			'li':	{},
			'pre':	{'font': ("Courier", DF[1], DF[2])},
			'center': {'justify': CENTER},
			'sub':	{'offset': -5},
			'sup':	{'offset': 5},
			'blockquote':	{'lmargin1': 20, 'lmargin2': 20,
					'rmargin':20,
					'font': (DF[0], DF[1], 'italic')},
		}

		# html tags that are block-level (as opposed to inline)
		self.BLOCKTAGS = ("h1","h2", "p", "ul", "ol", "li", "blockquote")

		HTMLParser.__init__(self)
		self.text = Text(master, wrap=WORD) # Parsed output will be sent to the Text widget
		self.buffer = ""
		self.tags = []
		self.images = []
		self.counter = 0	# for counting ol list (one level only!)
		self.is_ordered_list = False	# ol list, one level only!
		self.prev_was_newline = None
		self.is_in_pre = False	# for <pre> tag

		for s in self.STYLES.keys():
			#print s, self.STYLES[s]
			self.text.tag_config(s, self.STYLES[s])

	def feedfile(self, filename=None):
		self.basepath = os.path.dirname(os.path.abspath(filename))
		# read the contents
		if filename == None or filename == "":
			return

		try:
			f = open(filename, "r")
			contents = f.read()
			f.close()
		except:
			print "Can't open "+filename
			return

		HTMLParser.feed(self, contents)
		self.text.configure(state=DISABLED)
		#self.dump()

	def translateTag(self, tag):
		# Some tags are the same as others
		if tag == "strong":
			return "b"
		elif tag == "em":
			return "i"
		elif tag == "code":
			return "pre"
		return tag

	def handle_starttag(self, tag, attrs):
		#print "Start: <%s>" % tag
		#print "  Attr: %s" % attrs

		tag = self.translateTag(tag)

		# Print buffer into text widget
		if self.buffer != "":
			self.text.insert(INSERT, self.buffer)
		self.buffer = ""

		if self.is_in_pre:	# are we in a <pre> block?
			# this is not a 'real' tag, append it to the text and return
			self.text.insert(INSERT, '<'+tag+'>')
			return

		# Push tag into the stack, along with current position
		self.tags.append((tag, self.text.index(INSERT)))

		# First encounter! Configure the style first
		(uniqueTag, style) = self.getTagAndStyle()
		if tag != "pre":
			self.text.tag_configure(uniqueTag, style)
		else:
			# <pre> overrides the styles outside
			self.is_in_pre = True
			self.text.tag_configure(uniqueTag, self.STYLES["pre"])

		#print "  Tags: ", self.tags

		# Insert new text into buffer for the new tag
		if tag == "img":
			imgurl = None
			for (key, value) in attrs:
				#print key, value
				if key == "src":
					imgurl = value
			if imgurl != None:
				try:
					#print "Loading...", self.basepath+"/"+imgurl
					pic = PhotoImage(file=os.path.abspath(self.basepath+"/" +imgurl))
					label = Label(self.text, image=pic)
					label.image = pic
					self.images.append(label)
					self.text.window_create(END, window=label)
				except:
					self.buffer += " [img] "

		# Block tags get to start newlines
		if tag in self.BLOCKTAGS:
			if self.prev_was_newline == False:
				if tag == "li":
					self.buffer += "\n"
				else:
					self.buffer += "\n\n"
				self.prev_was_newline = True

			if tag == "ol":
				self.is_ordered_list = True
				self.counter = 0
			elif tag == "ul":
				self.is_ordered_list = False
			elif tag == "li":
				if self.is_ordered_list:
					self.counter += 1
					if len(str(self.counter)) < 2:
						self.buffer += " "
					self.buffer += str(self.counter)+". "
				else:
					self.buffer += "* "

		# If tag is not a block tag, we can reset prev_was_newline
		# Ignore non-printing header tags
		if (not tag in self.BLOCKTAGS) and (not tag in ("html","body","head","title")):
			self.prev_was_newline = False

	def handle_endtag(self, tag):
		#print "End: <%s>" % tag
		#print "  Stack: ", tuple(self.tags)
		#print "  Buffer: ", self.buffer

		tag = self.translateTag(tag)

		# Print buffer and insert the styles used for this buffer
		if self.buffer != "":
			self.text.insert(INSERT, self.buffer)

		if tag == 'pre':	# end <pre> block
			self.is_in_pre = False

		if self.is_in_pre:
			self.text.insert(INSERT, '</'+tag+'> ')
			self.buffer = ""
			return

		if self.tags != []:
			# style is marked from pos1 to pos2
			(uniqueTag, style) = self.getTagAndStyle()
			#self.text.tag_configure(uniqueTag, style)
			(tag1, pos1) = self.tags.pop()
			#print tag1, tag
			pos2 = self.text.index(INSERT)
			self.text.tag_add(uniqueTag, pos1, pos2)
		self.prev_was_newline = False

		if tag == "br":
			self.text.insert(INSERT, "\n")
		else:
			self.text.insert(INSERT, " ")

		self.buffer = ""

	def handle_data(self, data):
		#print "Data: '%s'" % data
		if not self.is_in_pre:
			# Remove leading whitespace and join multiple lines into one
			line = re.sub('\n+\s*', ' ', data)
			# Remove redundant whitespace
			line = re.sub('\s+', ' ', line)
			self.buffer += line.lstrip()
		else:
			self.buffer += data

	def handle_comment(self, data):
		#print "Comment: '%s'" % data
		# Ignore all comments
		return

	def dump(self):
		# Debug function - dump contents of text widget
		for i in self.text.dump("0.0", END):
			print i[2]+": ["+i[0]+"] "+i[1]

	def getTagAndStyle(self):
		# Create unique tag and style based on current nested tags
		newTag = ""
		newStyle = {}
		got_bold = False
		got_italic = False

		# iterate through self.tags in sequence
		for i in self.tags:
			newTag += i[0] + "#"	# Hash character as 'delimiter'
			# Merge each subsequent tag style
			if i[0] in self.STYLES:
				#print i[0],
				current_style = self.STYLES[i[0]]
				for s in current_style:
					# bold and italic tags override other font weights
					if i[0] in ("b","i") and s == 'font':
						if current_style[s][2] == 'bold':
							got_bold = True
						elif current_style[s][2] == 'italic':
							got_italic = True
					if s == 'font':
						newStyle[s] = list(current_style[s])
					else:
						newStyle[s] = current_style[s]

		if got_bold and got_italic:
			newStyle['font'][2] = 'bold italic'
		elif got_bold:
			newStyle['font'][2] = 'bold'
		elif got_italic:
			newStyle['font'][2] = 'italic'

		# Need to convert back to tuple for Mac - it will choke if font is a list
		newStyle['font'] = tuple(newStyle['font'])
		#print newTag, newStyle
		return (newTag, newStyle)

# View Html dialog to display contents of HTML file

class ViewHtmlDialog(SimpleDialogExt):
	contents = ""

	def __init__(self, parent, title=None, filename="", basefont=None):
		self.filename = filename
		self.basefont = basefont
		SimpleDialogExt.__init__(self, parent, title, text1="Close", text3="")

	def body(self, master):
		self.parser = SimpleTkHtml(master, self.basefont)
		self.parser.feedfile(self.filename)
		self.viewHtml = self.parser.text

		self.viewHtml.configure(width=70, height=20, bg="white")
		self.viewHtml.grid(row=0, column=0, sticky=N+S+E+W)

		self.viewScrollY = AutoScrollbar(master, orient=VERTICAL, command=self.viewHtml.yview)
		self.viewScrollY.grid(row=0, column=1, stick=NS)
		self.viewHtml["yscrollcommand"] = self.viewScrollY.set

		self.viewScrollX = AutoScrollbar(master, orient=HORIZONTAL, command=self.viewHtml.xview)
		self.viewScrollX.grid(row=1, column=0, stick=EW)
		self.viewHtml["xscrollcommand"] = self.viewScrollX.set

	def apply(self):
		return


# SelectFontDialog - selects a font with preview
# Returns a font:(font-family, size, style)

class SelectFontDialog(SimpleDialogExt):
	def __init__(self, parent, title=None, initfont=("Helvetica", "10", "normal")):
		self.selectedFont = ""
		self.isBold = False
		self.isItalic = False
		self.fontVar = StringVar()
		self.sizeVar = StringVar()
		self.boldVar = BooleanVar()
		self.italicVar = BooleanVar()
		self.font = initfont[0]
		self.size = initfont[1]
		self.style = initfont[2]

		if self.style == "bold italic":
			self.isBold = True
			self.isItalic = True
		elif self.style == "bold":
			self.isBold = True
		elif self.style == "italic":
			self.isItalic = True

		SimpleDialogExt.__init__(self, parent, title, text1="Select")

	def body(self, master):
		self.fontEntry = Entry(master, width=20, textvariable=self.fontVar)
		self.fontEntry.delete(0, END)
		self.fontEntry.insert(INSERT, self.font)
		self.fontEntry.grid(row=0, column=0, sticky=E+W)
		self.fontComboMenu = ComboMenu(master, attachto=self.fontEntry, text=">")
		self.fontComboMenu.setList(sorted(tkFont.families()))
		self.fontComboMenu.grid(row=0, column=1, sticky=W)

		self.sizeEntry = Entry(master, width=3, textvariable=self.sizeVar)
		self.sizeEntry.delete(0, END)
		self.sizeEntry.insert(INSERT, self.size)
		self.sizeEntry.grid(row=0, column=2, sticky=W)
		self.sizeComboMenu = ComboMenu(master, attachto=self.sizeEntry, text=">")
		self.sizeComboMenu.setList(map(str, range(8,73)))
		self.sizeComboMenu.grid(row=0, column=3, sticky=W)

		global icondir
		self.boldIcon = default_icons.getIcon("text-bold")
		self.italicIcon = default_icons.getIcon("text-italic")

		Checkbutton(master, text=" B ", indicatoron=False, variable=self.boldVar, image=self.boldIcon).grid(row=0, column=4)
		if self.isBold:
			self.boldVar.set(True)
		Checkbutton(master, text=" I ", indicatoron=False, variable=self.italicVar, image=self.italicIcon).grid(row=0, column=5)
		if self.isItalic:
			self.italicVar.set(True)

		#self.update_idletasks()

		Label(master, text="Preview:").grid(row=1, column=0, sticky=W)

		self.previewCanvas = Canvas(master, height=120, width=50, bg="white")
		self.previewFont = Label(self.previewCanvas, text="ABCDEFGHIJKLM\nNOPQRSTUVWXYZ\nabcdefghijklm\nnopqrstuvwxyz\n0123456789", bg="white", justify=LEFT, font=(self.font, self.size, self.style))
		self.previewCanvas.create_window((0,0), window=self.previewFont, anchor=NW)
		self.previewCanvas.grid(row=2, column=0, columnspan=6, sticky=E+W)

		self.viewScrollY = AutoScrollbar(master, orient=VERTICAL, command=self.previewCanvas.yview)
		self.viewScrollY.grid(row=2, column=7, stick=NS+W)
		self.previewCanvas["yscrollcommand"] = self.viewScrollY.set

		self.viewScrollX = AutoScrollbar(master, orient=HORIZONTAL, command=self.previewCanvas.xview)
		self.viewScrollX.grid(row=3, column=0, stick=EW)
		self.previewCanvas["xscrollcommand"] = self.viewScrollX.set

		# The Tk variables to monitor for changes (for updating Preview)
		self.fontVar.trace_variable("w", self.setPreview)
		self.sizeVar.trace_variable("w", self.setPreview)
		self.boldVar.trace_variable("w", self.setPreview)
		self.italicVar.trace_variable("w", self.setPreview)

	def setPreview(self, *dummy):
		self.font = self.fontVar.get()
		#print self.font
		if not self.font in tkFont.families():
			self.font = "Helvetica"
		self.size = self.sizeVar.get()
		if self.size == "":
			self.size = "10"

		self.isBold = self.boldVar.get()
		self.isItalic = self.italicVar.get()

		if self.isBold and self.isItalic:
			self.style = "bold italic"
		elif self.isBold:
			self.style = "bold"
		elif self.isItalic:
			self.style = "italic"
		else:
			self.style = "normal"

		self.previewFont.configure(font=(self.font, self.size, self.style))
		self.update_idletasks()
		self.previewCanvas.configure(scrollregion=self.previewCanvas.bbox(ALL))


	def apply(self):
		self.selectedFont = (self.font, self.size, self.style)
		return
