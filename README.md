# LeMMA - a GUI frontend for creating MMA files

> Announcement: The master branch has been ported to Python 3. The previous Python 2 is in the python2 branch.

_Note that this is NOT really an MMA editor, but rather a simple front-end to generate simple MMA files. I wrote this program so that I can churn out and play chord progressions easily._

# INSTALLATION

## Windows

Just unzip the files to any directory and run `lemma.pyw` or `lemma.py`

## Linux

Run `install.py` which will install to `/usr/local`

You can also use the command-line option `--prefix=/usr` to install to `/usr`

Or you can just unzip the files to a user directory and run `lemma.py` directly

Note that if you install to `/usr` or `/usr/local`, the configuration files will be saved in `~/.lemma`. This can be overridden with the the `--config` option when starting LeMMA.

To uninstall LeMMA manually, delete the file `<your install dir>/bin/lemma` and the directory `<your install dir>/share/lemma`

# USAGE

Usage: `lemma(.py) [options] [MMA file]`

Command-line options:
```
  --help		This help message
  --debug		Turns on debug mode (run this from a shell window)
  --config=dir	Use "dir" for configuration settings
```

Click on the "Help" button in the program for more information on usage.

---
Gek S. Low <geksiong@yahoo.com>
