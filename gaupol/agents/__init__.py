# -*- coding: utf-8 -*-

# Copyright (C) 2007 Osmo Salomaa
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

"""Extension delegates of of :class:`gaupol.Application`."""

from .close    import CloseAgent
from .edit     import EditAgent
from .format   import FormatAgent
from .help     import HelpAgent
from .menu     import MenuAgent
from .open     import OpenAgent
from .preview  import PreviewAgent
from .save     import SaveAgent
from .search   import SearchAgent
from .tools    import ToolsAgent
from .update   import UpdateAgent
from .util     import UtilityAgent
from .video    import VideoAgent
from .view     import ViewAgent

__all__ = tuple(x for x in dir() if x.endswith("Agent"))
