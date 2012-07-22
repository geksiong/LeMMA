# To make Debian package for LeMMA

sudo checkinstall -D --pkgname="lemma" --pkgversion="0.9a" --pkgarch="i686" --pkglicense="Others" --pkggroup="sound" --maintainer="Gek S. Low \<geksiong\@yahoo.com\>" --provides="lemma" --pkgsource="" --nodoc ./install.py --prefix="/usr"
