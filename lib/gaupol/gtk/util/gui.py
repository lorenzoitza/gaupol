# Copyright (C) 2005 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Gaupol is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gaupol; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Functions for GTK widgets."""


import gc
import logging
import os
import sys

import gtk
import gtk.glade

from gaupol.gtk.paths import GLADE_DIR


logger = logging.getLogger()

normal_cursor = gtk.gdk.Cursor(gtk.gdk.LEFT_PTR)
busy_cursor   = gtk.gdk.Cursor(gtk.gdk.WATCH)


def destroy_gobject(gobj):
    """Destroy gobject completely from memory."""

    # NOTE:
    # This is needed while PyGTK bug #320428 is unsolved.
    # http://bugzilla.gnome.org/show_bug.cgi?id=320428
    # http://bugzilla.gnome.org/attachment.cgi?id=18069

    try:
        gobj.destroy()
    except AttributeError:
        pass

    del gobj
    gc.collect()

def get_glade_xml(basename):
    """
    Get gtk.glade.XML object from basename in Glade directory.

    Raise RuntimeError if unable to load Glade XML file.
    """
    path = os.path.join(GLADE_DIR, basename)

    try:
        return gtk.glade.XML(path)
    except RuntimeError:
        logger.error('Failed to load Glade XML file "%s".' % path)
        raise

def get_event_box(widget):
    """Get EventBox if it is a parent of widget."""

    event_box = widget.get_parent()
    while not isinstance(event_box, gtk.EventBox):
        event_box = event_box.get_parent()

    return event_box

def get_parent_widget(child, parent_type):
    """Get parent of widget that is of given type."""

    parent = child.get_parent()
    while not isinstance(parent, parent_type):
        parent = parent.get_parent()

    return parent

def set_cursor_busy(window):
    """
    Set cursor busy when above window.

    window: gtk.Window
    """
    window.window.set_cursor(busy_cursor)

def set_cursor_normal(window):
    """
    Set cursor normal when above window.

    window: gtk.Window
    """
    window.window.set_cursor(normal_cursor)
