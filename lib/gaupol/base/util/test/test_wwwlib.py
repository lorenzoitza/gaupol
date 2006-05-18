# Copyright (C) 2005-2006 Osmo Salomaa
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


import urllib2

from gaupol.base.error import TimeoutError
from gaupol.base.util  import wwwlib
from gaupol.test       import Test


class TestModule(Test):

    def test_read_url(self):

        url = 'http://download.gna.org/gaupol/latest.txt'

        text = wwwlib.read_url(url, 10)
        assert isinstance(text, basestring)

        try:
            wwwlib.read_url(url, 0.001)
            raise AssertionError
        except TimeoutError:
            pass

        try:
            wwwlib.read_url(url + 'x', 10)
            raise AssertionError
        except urllib2.URLError:
            pass
