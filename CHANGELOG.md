# LeMMA - a GUI frontend for creating MMA files

Copyright (c) Gek S. Low

## 0.9 alpha (22 Aug 2010):
- Some minor bug fixes
- *FIXED*: Compatibility with python 2.4
- *NEW*: Transpose chords function
- *NEW*: Option to use PyGame module for midi playback instead of external midi player

## 0.8 alpha (27 July 2009):
- Many changes this round. I will attempt to categorise them below.
- Please note that there are changes to the settings and grooves database, so please re-do the settings.

**General**:
- "Renamed" LeMMA - it's no longer an acronym, since no one should be a "Lazy man" :-)
- Made an icon for LeMMA (I am so obviously not a graphics designer)
- Internal re-organisation of codes. lemma.pyw now imports lemma.py so there's no redundant codes.
- *FIXED*: Change order of LeMMA app path detection to check the current directory first instead of last, thus allowing different versions to be used. This should affect Linux systems only.
- *NEW*: Using ConfigParser for settings.dat (ini-like file format). Grooves database still using Pickler.

**GUI revamp**:
- New look and feel. Added application menu and toolbars. New 'about' window, html help, combo menus, spinboxes, etc. Little touches here and there.
- *NEW FEATURE*: Show/hide the output window
- *NEW FEATURE*: You can now select and save your preferred fonts for the GUI.
- *FIXED*: Use tkMessageBox.askyesno with tkMessageBox.okcancel. askyesno appears to have a bug that will always return false sometimes. okcancel seems to work correctly.
- *FIXED*: Use askdirectory instead of askopenfile when the intent is to select a directory.

**Initial Mac support (EXPERIMENTAL)**
- Custom flat button implementation that works for Mac platforms
- Automatic font upscaling for Mac platforms (by 1.33 times), since Mac fonts are usually displayed smaller. Mac users please feedback if this is ok or you prefer to use Mac font sizes. Also let me know which default fonts and sizes are best for Mac platform.

**Main edit window**:
- *NEW FEATURE*: Keyboard navigation and shortcuts.
- *NEW FEATURE*: Measure contents are validated against valid chord types and time signature when leaving the measure. Able to handle songs which starts with a slash instead of a chord. Invalid contents are highlighted in red.
- *NEW FEATURE*: Unused measures are now grayed out for easier reading.
- *NEW FEATURE*: You can adjust number of measures displayed per row. Default is now 4 measures per row to avoid horizontal scrolling in most cases. The initial number of measures can also be set in 'Settings'.
- *FIXED*: Improved scrolling of edit area. Also eliminated the 'jumping' around when loading MMA files.

**Grooves**:
- *NEW FEATURE*: Progress bar for groove refresh.
- *FIXED*: Groove files are now processed in alphabetical order.
- *FIXED*: No more crash when no grooves were found.
- *FIXED*: Auto rename groove library if name conflicts occur during refresh.
- *FIXED*: Groove name lookups are now case-insensitive. This affects the groove library file. You must refresh your grooves!
- *CHANGED*: Groove selection now sports a "Clear" button. "Cancel" will now leave the current groove as it is.
- *FIXED*: Temporary midi file is deleted first before generation. Midi player will only if launched if midi file was generated successfully.

**Loading and saving files**:
- *CHANGED*: Codes are now printed before grooves.
- *FIXED*: Code lines now preserve leading spaces and trailing newlines.
- *FIXED*: Groove lines with variables are now treated as code and will appear in the code section.
- *FIXED*: Code in last measure wasn't included in saved file.


## 0.7.1 (26 Mar 2009):
- *NEW FEATURE*: Support Linux installation in /usr and /usr/local, and store configuration files in ~/.lemma (auto-create). If installed anywhere else, config files are stored in application directory as in previous versions.
- *NEW FEATURE*: --config command-line option to override detected config directory
- *FIXED*: Configuration files were saved in current directory instead of application directory
- Install script and first Debian package

## 0.7 (1 Mar 2009):
- *NEW FEATURE*: You can now supply a filename at the command-line to load an MMA file on start
- *NEW FEATURE*: Auto-detect python, mma and mma grooves paths from Settings, and when settings.dat is absent. Note that there should be no need to modify python path now, but you can still modify it in the GUI if it is needed for whatever reasons.
- *NEW FEATURE*: You can edit and save the MMA grooves path in Settings (in case your default grooves are in an unusual location)
- *BUG FIX*: mmaDir not defined when determining mma lib path under Windows
- *BUG FIX*: midi file path for Windows was hardcoded with forward slash instead of backslash.
- *BUG FIX*: Removed extra double quotes when selecting midi player path
- *BUG FIX*: MMA version detection during grooves refresh not working correctly.
- *BUG FIX*: Added stderr and stdin to subprocess calls. Apparently this fixes some problems with pythonw.exe under Windows.
- settings.dat will no longer be distributed since it causes confusion for non-Linux users.
- Display currently loaded file on window title bar.
- grooves.dat updated to version 1.4.
- Always normalise OS path after file selection dialogs.
- Consolidated command to launch midiplayer.
- Better error handling:
	- When trying to set grooves when there are no grooves loaded.
	- More informational messages in output window.
	- Validate file paths at various interaction points before proceeding
	- Added debug logging. Use '--debug' option at command-line.
- Internal changes to groove dictionary format - store paths as \<default\> for grooves in the default mma library. GUI was changed accordingly.
- Changed platform detection to make Linux the default (should work for Macs, but I don't have one to test with) rather than Windows previously

## 0.6a (29 Feb 2008)
- Fixed incorrect detection of MMA 1.3 causing grooves search to fail
- Updated grooves library to MMA 1.3

## 0.6 Alpha (9 Feb 2008)
- *NEW FEATURE*: Support for custom groove library path (SetLibPath command)
- *NEW FEATURE*: Custom MMA commands can be assigned to each measure. Codes will be placed between the Groove command and the measure definition
- *NEW FEATURE*: View MMA function. Useful for previewing the generated code (and for my debugging)
- Various interface & usability improvements:
	- Standardised fonts and colors
	- Revamp of main editing window
	- Change in input method: You can click toggle the barlines type instead of entering them into the measures
	- Automatic scrolling in many places
- More editing space - 8 measures x 10 rows
- Groove selection now automatically goes to the assigned groove and pre-selects the current groove
- *FILE FORMAT*: Path of groove source files and a reverse lookup table added to grooves.dat, to support the new library switching features
- *FILE FORMAT*: Custom groove library path added to settings.dat
- *BUG FIX*: Default groove library path search now follows the MMA documentation
- *BUG FIX*: Load MMA file will no longer clear current file if cancelled
- *BUG FIX*: Save MMA will no longer try to save file if cancelled
- *BUG FIX*: Grooves are sorted correctly now in listbox
- *BUG FIX*: Use of SetAutoLibPath command to switch between stdlib and other groove libraries in default grooves library path (previously it can pick up the groove, but did not generate the correct codes for MMA to play them)
- Some code cleanup and internal re-organisation
- Various "constants" are defined and kept in separate constants.py file

## 0.5 (8 Dec 07)
- Grooves are now read from higher level lib folder instead of stdlib, so that other grooves libraries can be picked up
- Various fixes to enable LeMMA to run on Linux platforms
- For Linux, LeMMA will search \<mmapath\>/lib, /usr/share/mma/lib, /usr/local/share/mma/lib in that order for grooves files
- Grouped the grooves menu alphabetically to avoid menus being too long to fit on screen
- Change in the handling of midi players. Previously quotes were automatically inserted as many Windows programs reside in "Program Files" folder. To allow the use of command-line options (you have to manually edit the text field yourself), quotes are now inserted directly into the text field. Please re-configure your settings.

## 0.4 (21 Apr 07)
- Added output window at the bottom so that LeMMA can be run without a shell.
- Using os.popen now instead of subprocess.popen. Subprocess doesn't appear to work with .pyw files under Windows.
- MMA 1.1 uses -Dxl and MMA 1.0 uses -Dx. Added version check to decide which command-line option to use.
- Added help page.

## 0.3 (15 Apr 2007)
- main.py is now called lemma.py
- Added !# line for unix/linux users

## 0.2 (6 Apr 2007)
- Added "Load MMA" functionality to load previously saved MMA files (note that this will only load stuff that is recognised, meaning if you load files that are not created with this app you will most probably lose data when you resave.
- SwingMode Off now saved to support load function
- Groove defaults to Folk if no groove is set in first measure

## 0.1 (1 Apr 2007)
- Initial release

