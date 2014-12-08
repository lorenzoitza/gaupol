On the aeidon Package
=====================

aeidon is a Python package for reading, writing and manipulating
text-based subtitle files. It is used by the gaupol package, which
provides a a subtitle editor application with a GTK+ user interface.

Separating a user-interface independent general-purpose subtitle editing
package from Gaupol has been an afterthought and thus not well designed
to be a reusable component, but on the other hand is proven, working and
maintained code.

Installation
============

To install only either the aeidon or the gaupol package, use one
of the following commands

    python3 setup.py --without-gaupol clean install [--prefix=...]
    python3 setup.py --without-aeidon clean install [--prefix=...]

Note that the `--with-*` and `--without-*` are global options and must
be placed before any commands.

Dependencies of aeidon and gaupol as Separate Packages
======================================================

Of the dependencies listed in the `README.md` file, Python, PyEnchant,
iso-codes and chardet are to be associated with aeidon. If aeidon is
installed using the `--without-iso-codes` switch, then iso-codes is
required instead of optional.

Likewise, Python, PyGObject, GTK+, GStreamer, GtkSpell, MPlayer, VLC
and PT Sans Caption and PT Mono fonts are to be associated with gaupol.
gaupol also requires aeidon of the exact same version.