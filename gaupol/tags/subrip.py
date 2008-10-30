# Copyright (C) 2005-2008 Osmo Salomaa
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

"""Text markup for the SubRip format."""

import gaupol
import re

__all__ = ("SubRip",)


class SubRip(gaupol.Markup):

    """Text markup for the SubRip format.

    SubRip format is assumed (based on the SubRip application GUI) to contain
    the following HTML-style tags, in either lower- or upper case.

     * <b>.........................</b>
     * <i>.........................</i>
     * <u>.........................</u>
     * <font color="#RRGGBB">...</font>
    """

    _flags = re.DOTALL | re.MULTILINE | re.UNICODE | re.IGNORECASE
    format = gaupol.formats.SUBRIP

    def _main_decode(self, text):
        """Return text with decodable markup decoded."""

        text = self._decode_b(text, r"<b>(.*?)</b>", 1)
        text = self._decode_i(text, r"<i>(.*?)</i>", 1)
        text = self._decode_u(text, r"<u>(.*?)</u>", 1)
        pattern = r'<font color="#([0-9a-fA-F]{6})">(.*?)</font>'
        return self._decode_c(text, pattern, 1, 2)

    def bolden(self, text, bounds=None):
        """Return bolded text."""

        a, z = bounds or (0, len(text))
        return "".join((text[:a], "<b>%s</b>" % text[a:z], text[z:]))

    def clean(self, text):
        """Return text with less ugly markup."""

        # Remove tags that are immeadiately closed after opening.
        text = self._substitute(text, r"<([a-z]+)[^<]*?>( *)</\1>", r"\2")
        # Remove tags that are immeadiately opened after closing.
        text = self._substitute(text, r"</([a-z]+)>( *)<\1[^<]*?>", r"\2")
        # Remove or relocate space right after an opening tag.
        text = self._substitute(text, r" ?(<(?!/)[^>]+?>) ", r" \1")
        # Remove or relocate space right before a closing tag.
        return self._substitute(text, r" (</[^>]+?>) ?", r"\1 ")

    def colorize(self, text, color, bounds=None):
        """Return text colorized to hexadecimal value."""

        a, z = bounds or (0, len(text))
        target = '<font color="#%s">%s</font>' % (color, text[a:z])
        return "".join((text[:a], target, text[z:]))

    @property
    def italic_tag(self):
        """Regular expression for an italic markup tag."""

        return self._get_regex(r"</?i>")

    def italicize(self, text, bounds=None):
        """Return italicized text."""

        a, z = bounds or (0, len(text))
        return "".join((text[:a], "<i>%s</i>" % text[a:z], text[z:]))

    @property
    def tag(self):
        """Regular expression for any markup tag."""

        return self._get_regex(r"<.*?>")

    def underline(self, text, bounds=None):
        """Return underlined text."""

        a, z = bounds or (0, len(text))
        return "".join((text[:a], "<u>%s</u>" % text[a:z], text[z:]))
