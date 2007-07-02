# Copyright (C) 2005-2007 Osmo Salomaa
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


import functools
import gaupol.gtk
import gtk

from gaupol.gtk import unittest


class TestOpenAgent(unittest.TestCase):

    def run__show_encoding_error_dialog(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_encoding_error_dialog("test")

    def run__show_format_error_dialog(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_format_error_dialog("test")

    def run__show_io_error_dialog(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_io_error_dialog("test", "test")

    def run__show_parse_error_dialog(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        format = gaupol.gtk.FORMAT.SUBRIP
        self.delegate._show_parse_error_dialog("test", format)

    @gaupol.gtk.util.silent(gaupol.gtk.Default)
    def run__show_size_warning_dialog(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_size_warning_dialog("test", 2)

    @gaupol.gtk.util.silent(gaupol.gtk.Default)
    def run__show_sort_warning_dialog(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_sort_warning_dialog("test", 3)

    @gaupol.gtk.util.silent(gaupol.gtk.Default)
    def run__show_ssa_warning_dialog(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        self.delegate._show_ssa_warning_dialog()

    @gaupol.gtk.util.silent(gaupol.gtk.Default)
    def run__show_translation_warning_dialog(self):

        flash_dialog = gaupol.gtk.Runner.flash_dialog
        flash_dialog = functools.partial(flash_dialog, self.application)
        self.delegate.flash_dialog = flash_dialog
        page = self.application.get_current_page()
        self.delegate._show_translation_warning_dialog(page)

    def setup_method(self, method):

        self.application = self.get_application()
        self.delegate = self.application.open_main_files.im_self
        respond = lambda *args: gtk.RESPONSE_DELETE_EVENT
        self.delegate.flash_dialog = respond
        self.delegate.run_dialog = respond

    def test__ensure_file_not_open(self):

        path = self.get_subrip_path()
        self.delegate._ensure_file_not_open(path)
        self.application.open_main_file(path)
        function = self.delegate._ensure_file_not_open
        self.raises(gaupol.gtk.Default, function, path)

    def test__get_encodings(self):

        self.delegate._get_encodings()
        self.delegate._get_encodings("johab")

    def test__show_encoding_error_dialog(self):

        self.delegate._show_encoding_error_dialog("test")

    def test__show_format_error_dialog(self):

        self.delegate._show_format_error_dialog("test")

    def test__show_io_error_dialog(self):

        self.delegate._show_io_error_dialog("test", "test")

    def test__show_parse_error_dialog(self):

        format = gaupol.gtk.FORMAT.SUBRIP
        self.delegate._show_parse_error_dialog("test", format)

    @gaupol.gtk.util.silent(gaupol.gtk.Default)
    def test__show_size_warning_dialog(self):

        self.delegate._show_size_warning_dialog("test", 2)

    @gaupol.gtk.util.silent(gaupol.gtk.Default)
    def test__show_sort_warning_dialog(self):

        self.delegate._show_sort_warning_dialog("test", 3)

    @gaupol.gtk.util.silent(gaupol.gtk.Default)
    def test__show_ssa_warning_dialog(self):

        self.delegate._show_ssa_warning_dialog()

    @gaupol.gtk.util.silent(gaupol.gtk.Default)
    def test__show_translation_warning_dialog(self):

        page = self.application.get_current_page()
        self.delegate._show_translation_warning_dialog(page)

    def test_add_new_page(self):

        self.application.add_new_page(self.get_page())

    def test_add_to_recent_files(self):

        path = self.get_subrip_path()
        self.delegate.add_to_recent_files(path, gaupol.gtk.DOCUMENT.MAIN)
        self.delegate.add_to_recent_files(path, gaupol.gtk.DOCUMENT.TRAN)

    def test_connect_to_view_signals(self):

        view = self.application.pages[0].view
        self.application.connect_to_view_signals(view)

    def test_on_append_file_activate(self):

        self.application.on_append_file_activate()

    def test_on_new_project_activate(self):

        self.application.on_new_project_activate()

    def test_on_open_main_files_activate(self):

        self.application.on_open_main_files_activate()

    def test_on_open_translation_file_activate(self):

        self.application.on_open_translation_file_activate()

    @gaupol.gtk.util.asserted_return
    def test_on_recent_main_menu_item_activated(self):

        name = "show_recent_main_menu"
        menu = self.application.get_menu_item(name).get_submenu()
        assert menu.get_children()
        item = menu.get_children()[0]
        menu.activate_item(item, True)

    @gaupol.gtk.util.asserted_return
    def test_on_recent_translation_menu_item_activated(self):

        name = "show_recent_translation_menu"
        menu = self.application.get_menu_item(name).get_submenu()
        assert menu.get_children()
        item = menu.get_children()[0]
        menu.activate_item(item, True)

    def test_on_select_video_file_activate(self):

        self.application.on_select_video_file_activate()

    def test_on_split_project_activate(self):

        responder = iter((gtk.RESPONSE_OK, gtk.RESPONSE_CANCEL))
        flash_dialog = lambda *args: responder.next()
        self.delegate.flash_dialog = flash_dialog
        self.application.pages[0].view.select_rows([3])
        self.application.on_split_project_activate()
        self.application.on_split_project_activate()

    def test_on_video_button_clicked(self):

        self.application.on_video_button_clicked()

    def test_open_main_file(self):

        self.application.open_main_file(self.get_subrip_path())
        self.application.open_main_file(self.get_subrip_path(), "ascii")

    def test_open_main_files(self):

        paths = (self.get_subrip_path(), self.get_microdvd_path())
        self.application.open_main_files(paths)
        self.application.open_main_files(paths, "ascii")

    def test_open_translation_file(self):

        path = self.get_subrip_path()
        self.application.open_translation_file(path)
        self.application.open_translation_file(path, "ascii")
