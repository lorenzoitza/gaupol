# Copyright (C) 2006 Osmo Salomaa
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
# A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# Gaupol.  If not, see <http://www.gnu.org/licenses/>.


import urllib

from gaupol import unittest
from .. import urls


class TestModule(unittest.TestCase):

    def test_attributes(self):

        urllib.urlopen(urls.BUG_REPORT_URL)
        urllib.urlopen(urls.HOMEPAGE_URL)
        urllib.urlopen(urls.REGEX_HELP_URL)
