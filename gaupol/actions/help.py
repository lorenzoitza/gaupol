# -*- coding: utf-8 -*-

# Copyright (C) 2005 Osmo Salomaa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Help actions for :class:`gaupol.Application`."""

import gaupol

class BrowseDocumentationAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "browse_documentation")
        self.action_group = "main-safe"

class ReportABugAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "report_a_bug")
        self.action_group = "main-safe"

class ViewAboutDialogAction(gaupol.Action):
    def __init__(self):
        gaupol.Action.__init__(self, "view_about_dialog")
        self.action_group = "main-safe"

__all__ = tuple(x for x in dir() if x.endswith("Action"))
