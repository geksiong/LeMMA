# constants.py
"""
Central location for all constants

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

import platform

# Layout
DEFAULT_MEASURE_WIDTH = 12
#MEASURES_PER_ROW = 4
MEASURES_TOTAL = 100

# Fonts
FONT_SIZE_MIN = 8
FONT_SIZE_MAX = 144

FONTKEYS = ["Base", "Text", "Groove", "Code", "Measure number", "Bar", "Measure"]

FONTS = {
	"Base": ("Helvetica", "9", "normal"),
	"Text": ("Helvetica", "9", "normal"),
	"Groove": ("Helvetica", "8", "bold"),
	"Groove None": ("Helvetica", "8", "normal"),
	"Code": ("Courier", "8", "bold"),
	"Code None": ("Courier", "8", "normal"),
	"Measure number": ("Helvetica", "8", "normal"),
	"Bar": ("Helvetica", "13", "bold"),
	"Measure": ("Helvetica", "13", "normal"),
	}

def autoScaleFont(font):
	# Checks for Mac and automatically scales the font up by 1.33x
	# To be used dynamically. Don't modify the FONTS dictionary itself.
	if platform.system() in ('Darwin'):
		return (font[0], str(int(font[1]) * 4 // 3), font[2])
	else:
		return font

# In main editing window
BARLINE_COLOR_FG = "black"
BARLINE_COLOR_BG = "white"
BARLINE_COLOR_FG_INACTIVE = "gray"
BARLINE_COLOR_BG_MOUSEENTER = "cyan"

BARNUM_COLOR_FG = "black"
BARNUM_COLOR_BG = "white"
BARNUM_COLOR_FG_INACTIVE = "gray"

GROOVE_COLOR_FG = "black"
GROOVE_COLOR_FG_NONE = "gray"
GROOVE_COLOR_BG = "white"
GROOVE_COLOR_BG_MOUSEENTER = "cyan"
GROOVE_TEXT_NONE = " (Groove) "

CODE_COLOR_FG = "black"
CODE_COLOR_FG_NONE = "gray"
CODE_COLOR_BG = "white"
CODE_COLOR_BG_MOUSEENTER = "cyan"
CODE_TEXT = " <Code> "

MEASURE_COLOR_FG = "black"
MEASURE_COLOR_FG_ERROR = "red"
MEASURE_COLOR_BG = "white"
MEASURE_COLOR_BG_FOCUS = "yellow"
MEASURE_COLOR_HIGHLIGHT_MOUSEENTER = "black"
MEASURE_COLOR_HIGHLIGHT = "white"

MAINFRAME_COLOR_BG = "white"

CHORDTYPES = set(['', 'maj', 'min', '#5', '(b5)', '+', '+7', '+7b9#11', '+9',
	'+9M7', '+M7', '11', '11b9', '13', '13#11', '13#9', '13b5', '13b9',
	'13sus', '13susb9', '5', '6', '6(add9)', '69', '6/9', '7', '7#11',
	'7#5', '7#5#9', '7#5b9', '7#9', '7#9#11', '7#9b13', '7(omit3)', '7+',
	'7+5', '7+9', '7-5', '7-9', '7alt', '7b5', '7b5#9', '7b5b9', '7b9',
	'7b9#11', '7sus', '7sus2', '7sus4', '7sus9', '9', '9#11', '9#5',
	'9+5', '9-5', '9b5', '9sus', '9sus4', 'M13', 'M13#11', 'M6', 'M7',
	'M7#11', 'M7#5', 'M7(add13)', 'M7+5', 'M7-5', 'M7b5', 'M9', 'M9#11',
	'add9', 'aug', 'aug7', 'aug7#9', 'aug7b9', 'aug9', 'aug9M7', 'dim',
	'dim7', 'dim7(addM7)', 'm', 'm#5', 'm#7', 'm(add9)', 'm(b5)', 'm(maj7)',
	'm(sus9)', 'm+5', 'm+7', 'm+7#9', 'm+7b9', 'm+7b9#11', 'm11', 'm11b5',
	'm13', 'm6', 'm6(add9)', 'm69', 'm6/9', 'm7', 'm7#9', 'm7(#9)',
	'm7(add11)', 'm7(add13)', 'm7(b9)', 'm7(omit5)', 'm7-5', 'm7b5',
	'm7b5b9', 'm7b9', 'm7b9#11', 'm7omit5', 'm9', 'm9#11', 'mM7', 'mM7(add9)',
	'maj13', 'maj7', 'maj9', 'mb5', 'min#7', 'min(maj7)', 'omit3(add9)', 'omit3add9', 'sus', 'sus2', 'sus4', 'sus9'])
