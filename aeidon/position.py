# Copyright (C) 2011 Osmo Salomaa
#
# This file is part of Gaupol.
#
# Gaupol is free software: you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# Gaupol is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
# A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol. If not, see <http://www.gnu.org/licenses/>.

"""Mapping position types to basic Python types."""

# aeidon handles frames as integers, seconds as floats and times as strings.
# Some functions accept a "position" argument, which will be interpreted based
# on its type. These functions are introduced here so that callers can use as_*
# to ensure argument types and functions can use is_* to check argument types,
# all in a way which is compatible with the old ambiguous way of using int and
# float directly.

__all__ = ("as_frame",
           "as_seconds",
           "as_time",
           "is_frame",
           "is_seconds",
           "is_time")

def as_frame(frame):
    """Return `frame` as frame."""
    return int(frame)

def as_seconds(seconds):
    """Return `seconds` as seconds."""
    return float(seconds)

def as_time(time):
    """Return `time` as time."""
    return str(time)

def is_frame(pos):
    """Return ``True`` if `pos` is frame."""
    return isinstance(pos, int)

def is_seconds(pos):
    """Return ``True`` if `pos` is seconds."""
    return isinstance(pos, float)

def is_time(pos):
    """Return ``True`` if `pos` is time."""
    return isinstance(pos, str)