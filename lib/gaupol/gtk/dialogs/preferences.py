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


"""Dialog for editing preferences."""


try:
    from psyco.classes import *
except ImportError:
    pass

import gobject
import gtk
import pango

from gaupol.base.util            import encodinglib
from gaupol.constants            import VideoPlayer
from gaupol.gtk.dialogs.encoding import EncodingDialog
from gaupol.gtk.util             import config, gtklib


class PreferencesDialog(gobject.GObject):

    """
    Dialog for changing settings.

    This class is implemented as a GObject. All setting-changing events will
    send signals upstream, where they can be instant-applied.
    """

    __gsignals__ = {
        'destroyed': (
            gobject.SIGNAL_RUN_LAST,
            None,
            ()
        ),
        'limit-undo-toggled': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (gobject.TYPE_BOOLEAN,)
        ),
        'undo-levels-changed': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (gobject.TYPE_INT,)
        ),
        'use-default-font-toggled': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (gobject.TYPE_BOOLEAN,)
        ),
        'font-set': (
            gobject.SIGNAL_RUN_LAST,
            None,
            (gobject.TYPE_STRING,)
        )
    }

    def __init__(self, parent):

        gobject.GObject.__init__(self)

        glade_xml = gtklib.get_glade_xml('preferences-dialog.glade')
        get = glade_xml.get_widget

        # Widgets
        self._close_button             = get('close_button')
        self._dialog                   = get('dialog')
        self._encoding_add_button      = get('encoding_add_button')
        self._encoding_down_button     = get('encoding_move_down_button')
        self._encoding_locale_check    = get('encoding_locale_check_button')
        self._encoding_remove_button   = get('encoding_remove_button')
        self._encoding_up_button       = get('encoding_move_up_button')
        self._encoding_view            = get('encoding_tree_view')
        self._font_button              = get('font_button')
        self._font_custom_label        = get('font_custom_label')
        self._font_default_check       = get('font_default_check_button')
        self._preview_command_entry    = get('preview_command_entry')
        self._preview_command_legend   = get('preview_command_legend_table')
        self._preview_command_radio    = get('preview_command_radio_button')
        self._preview_customize_button = get('preview_customize_button')
        self._preview_offset_spin      = get('preview_offset_spin_button')
        self._preview_select_combo     = get('preview_select_combo_box')
        self._preview_select_radio     = get('preview_select_radio_button')
        self._undo_levels_spin         = get('undo_levels_spin_button')
        self._undo_limit_radio         = get('undo_limit_radio_button')
        self._undo_unlimited_radio     = get('undo_unlimited_radio_button')

        self._init_encoding_view()
        self._init_mnemonics(glade_xml)
        self._init_radio_groups()
        self._init_values()
        self._init_signals()
        self._dialog.set_transient_for(parent)
        self._dialog.set_default_response(gtk.RESPONSE_CLOSE)

    def _init_editor_signals(self):
        """Initialize editor tab signals."""

        # Undo limit radio button
        method = self._on_undo_limit_radio_toggled
        self._undo_limit_radio.connect('toggled', method)

        # Undo levels spin button
        method = self._on_undo_levels_spin_value_changed
        self._undo_levels_spin.connect('value-changed', method)

        # Font default check button
        method = self._on_font_default_check_toggled
        self._font_default_check.connect('toggled', method)

        # Font button
        method = self._on_font_button_font_set
        self._font_button.connect('font-set', method)

    def _init_editor_values(self):
        """Initialize editor tab widget values."""

        # Limit undo
        limit = config.editor.limit_undo
        self._undo_limit_radio.set_active(limit)
        self._undo_unlimited_radio.set_active(not limit)
        self._undo_levels_spin.set_sensitive(limit)

        # Undo levels
        self._undo_levels_spin.set_value(config.editor.undo_levels)

        # Use default/custom font
        use_default = config.editor.use_default_font
        self._font_default_check.set_active(use_default)
        self._font_custom_label.set_sensitive(not use_default)
        self._font_button.set_sensitive(not use_default)

        # Font
        self._font_button.set_font_name(self._get_custom_font())

    def _init_encoding_view(self):
        """Initialize encoding view."""

        view = self._encoding_view
        view.columns_autosize()

        selection = view.get_selection()
        selection.set_mode(gtk.SELECTION_SINGLE)
        selection.unselect_all()

        store = gtk.ListStore(gobject.TYPE_STRING)
        view.set_model(store)

        cell_renderer = gtk.CellRendererText()
        tree_view_column = gtk.TreeViewColumn('', cell_renderer, text=0)
        view.append_column(tree_view_column)

    def _init_file_signals(self):
        """Initialize file tab signals."""

        # Locale encoding check button
        method = self._on_encoding_locale_check_toggled
        self._encoding_locale_check.connect('toggled', method)

        # Encoding move buttons
        method = self._on_encoding_up_button_clicked
        self._encoding_up_button.connect('clicked', method)
        method = self._on_encoding_down_button_clicked
        self._encoding_down_button.connect('clicked', method)

        # Encoding add and remove buttons
        method = self._on_encoding_remove_button_clicked
        self._encoding_remove_button.connect('clicked', method)
        method = self._on_encoding_add_button_clicked
        self._encoding_add_button.connect('clicked', method)

    def _init_file_values(self):
        """Initialize file tab widget values."""

        # Locale encoding
        try_locale = config.file.try_locale_encoding
        self._encoding_locale_check.set_active(try_locale)

        # Fallback encodings
        self._reload_encoding_view()

    def _init_mnemonics(self, glade_xml):
        """Initialize mnemonics."""

        # Encoding view
        label = glade_xml.get_widget('encoding_label')
        label.set_mnemonic_widget(self._encoding_view)

        # Undo levels spin button
        label = glade_xml.get_widget('undo_levels_label')
        label.set_mnemonic_widget(self._undo_levels_spin)

        # Font button
        self._font_custom_label.set_mnemonic_widget(self._font_button)

        # Preview offset label
        label = glade_xml.get_widget('preview_offset_label')
        label.set_mnemonic_widget(self._preview_offset_spin)

    def _init_preview_signals(self):
        """Initialize preview tab signals."""

        # Offset spin button
        method = self._on_preview_offset_spin_value_changed
        self._preview_offset_spin.connect('value-changed', method)

        # Select radio button
        method = self._on_preview_select_radio_toggled
        self._preview_select_radio.connect('toggled', method)

        # Select combo box
        method = self._on_preview_select_combo_changed
        self._preview_select_combo.connect('changed', method)

        # Customize button
        method = self._on_preview_customize_button_clicked
        self._preview_customize_button.connect('clicked', method)

        # Command entry
        method = self._on_preview_command_entry_changed
        self._preview_command_entry.connect('changed', method)

    def _init_preview_values(self):
        """Initialize preview tab widget values."""

        # Offset
        self._preview_offset_spin.set_value(float(config.preview.offset))

        # Select or custom
        use_custom = config.preview.use_custom
        self._preview_select_radio.set_active(not use_custom)
        self._preview_command_radio.set_active(use_custom)
        self._set_preview_radio_sensitivities()

        # Video player
        for i, name in enumerate(VideoPlayer.display_names):
            self._preview_select_combo.insert_text(i, name)
        self._preview_select_combo.set_active(config.preview.video_player)

        # Command
        command = config.preview.custom_command
        self._preview_command_entry.set_text(command or '')

    def _init_radio_groups(self):
        """Initialize radio button groups."""

        # ValueError is raised if button already is in group.

        # Undo limiting
        group = self._undo_limit_radio.get_group()[0]
        try:
            self._undo_unlimited_radio.set_group(group)
        except ValueError:
            pass

        # Preview
        group = self._preview_select_radio.get_group()[0]
        try:
            self._preview_command_radio.set_group(group)
        except ValueError:
            pass

    def _init_signals(self):
        """Initialize signals."""

        self._init_editor_signals()
        self._init_file_signals()
        self._init_preview_signals()

        # Encoding view
        selection =  self._encoding_view.get_selection()
        method = self._on_encoding_view_selection_changed
        selection.connect('changed', method)

        # Close button
        self._close_button.connect('clicked', self._destroy)

        # Dialog
        self._dialog.connect('delete-event', self._destroy)

    def _init_values(self):
        """Initialize widget values."""

        self._init_file_values()
        self._init_editor_values()
        self._init_preview_values()

    def _destroy(self, *args):
        """Destroy the dialog."""

        self._dialog.destroy()
        self.emit('destroyed')

    def _get_custom_font(self):
        """
        Get custom font.

        This method merges the custom font setting with the default font
        taken from a random widget to create to complete font description
        string.
        Return font description as a string.
        """
        # Get the default font description from a random widget.
        context = self._font_custom_label.get_pango_context()
        font_description = context.get_font_description()

        # Create custom font description and merge that with the default.
        custom_font_description = pango.FontDescription(config.editor.font)
        font_description.merge(custom_font_description, True)

        return font_description.to_string()

    def _get_selected_encoding_row(self):
        """Get the selected fallback encoding view row."""

        selection = self._encoding_view.get_selection()
        store, itr = selection.get_selected()

        if itr is None:
            return None

        row = store.get_path(itr)
        try:
            return row[0]
        except TypeError:
            return row

    def _on_encoding_add_button_clicked(self, *args):
        """Add a new fallback encoding."""

        dialog = EncodingDialog(self._dialog)
        response = dialog.run()
        encoding = dialog.get_encoding()
        dialog.destroy()

        if response != gtk.RESPONSE_OK:
            return
        if encoding is None:
            return

        config.file.fallback_encodings.append(encoding)
        self._reload_encoding_view()

    def _on_encoding_down_button_clicked(self, *args):
        """Move the selected encoding down in the list."""

        source_row = self._get_selected_encoding_row()
        encodings = config.file.fallback_encodings
        encodings.insert(source_row + 1, encodings.pop(source_row))
        self._reload_encoding_view()

        self._encoding_view.grab_focus()
        selection = self._encoding_view.get_selection()
        selection.select_path(source_row + 1)

    def _on_encoding_locale_check_toggled(self, check_button):
        """Set use/don't use locale encoding."""

        config.file.try_locale_encoding = check_button.get_active()

    def _on_encoding_remove_button_clicked(self, *args):
        """Remove the selected encoding."""

        row = self._get_selected_encoding_row()
        config.file.fallback_encodings.pop(row)
        self._reload_encoding_view()

    def _on_encoding_up_button_clicked(self, *args):
        """Move the selected encoding up in the list."""

        source_row = self._get_selected_encoding_row()
        encodings = config.file.fallback_encodings
        encodings.insert(source_row - 1, encodings.pop(source_row))
        self._reload_encoding_view()

        self._encoding_view.grab_focus()
        selection = self._encoding_view.get_selection()
        selection.select_path(source_row - 1)

    def _on_encoding_view_selection_changed(self, *args):
        """Set sensitivities based on current selection."""

        self._set_encoding_button_sensitivities()

    def _on_font_button_font_set(self, font_button):
        """Set custom font and emit signal."""

        font = font_button.get_font_name()
        config.editor.font = font
        self.emit('font-set', font)

    def _on_font_default_check_toggled(self, check_button):
        """Set default/custom font and send signal."""

        use_default = check_button.get_active()
        self._font_custom_label.set_sensitive(not use_default)
        self._font_button.set_sensitive(not use_default)

        config.editor.use_default_font = use_default
        self.emit('use-default-font-toggled', use_default)

    def _on_preview_command_entry_changed(self, entry):
        """Set preview command."""

        config.preview.custom_command = entry.get_text() or None

    def _on_preview_customize_button_clicked(self, button):
        """Customize command."""

        video_player = self._preview_select_combo.get_active()
        command = VideoPlayer.commands[video_player]

        self._preview_command_entry.set_text(command)
        self._preview_command_radio.set_active(True)

    def _on_preview_offset_spin_value_changed(self, spin_button):
        """Set preview offset."""

        spin_button.update()
        value = '%.1f' % spin_button.get_value()
        config.preview.offset = value

    def _on_preview_select_combo_changed(self, combo_box):
        """Select video player."""

        config.preview.video_player = combo_box.get_active()

    def _on_preview_select_radio_toggled(self, radio_button):
        """Set use selected or custom video player."""

        use_custom = self._preview_command_radio.get_active()
        config.preview.use_custom = use_custom
        self._set_preview_radio_sensitivities()

        if use_custom:
            self._preview_command_entry.grab_focus()
        else:
            self._preview_select_combo.grab_focus()

    def _on_undo_levels_spin_value_changed(self, spin_button):
        """Set the amount of undo levels and send signal."""

        spin_button.update()
        levels = spin_button.get_value_as_int()

        config.editor.undo_levels = levels
        self.emit('undo-levels-changed', levels)

    def _on_undo_limit_radio_toggled(self, radio_button):
        """Limit/unlimit undo and send signal."""

        limit = self._undo_limit_radio.get_active()
        self._undo_levels_spin.set_sensitive(limit)

        config.editor.limit_undo = limit
        self.emit('limit-undo-toggled', limit)

    def _reload_encoding_view(self):
        """Reload the list of fallback encodings."""

        store = self._encoding_view.get_model()
        store.clear()
        for encoding in config.file.fallback_encodings:
            name = encodinglib.get_descriptive_name(encoding)
            store.append([name])

        self._set_encoding_button_sensitivities()

    def _set_encoding_button_sensitivities(self):
        """Set sensitivities of the fallback encoding view buttons."""

        store = self._encoding_view.get_model()

        if len(store) == 0:
            self._encoding_up_button.set_sensitive(False)
            self._encoding_down_button.set_sensitive(False)
            self._encoding_remove_button.set_sensitive(False)
            return

        row = self._get_selected_encoding_row()
        last_row = len(store) - 1

        self._encoding_up_button.set_sensitive(not row == 0)
        self._encoding_down_button.set_sensitive(not row == last_row)
        self._encoding_remove_button.set_sensitive(not row is None)

    def _set_preview_radio_sensitivities(self):
        """Set sensitivities depending on preview radio buttons."""

        if config.preview.use_custom:
            self._preview_select_combo.set_sensitive(False)
            self._preview_customize_button.set_sensitive(False)
            self._preview_command_entry.set_sensitive(True)
            self._preview_command_legend.set_sensitive(True)
        else:
            self._preview_select_combo.set_sensitive(True)
            self._preview_customize_button.set_sensitive(True)
            self._preview_command_entry.set_sensitive(False)
            self._preview_command_legend.set_sensitive(False)

    def show(self):
        """Show the dialog."""

        self._dialog.show()


if __name__ == '__main__':

    from gaupol.test import Test

    class TestPreferencesDialog(Test):

        def __init__(self):

            Test.__init__(self)
            self.dialog = PreferencesDialog(gtk.Window())
            self.dialog.show()

        def destroy(self):

            self.dialog._close_button.emit('clicked')

        def test_get_custom_font(self):

            font = self.dialog._get_custom_font()
            assert isinstance(font, basestring)

        def test_get_selected_encoding(self):

            selection = self.dialog._encoding_view.get_selection()
            selection.unselect_all()
            assert self.dialog._get_selected_encoding_row() is None
            selection.select_path(0)
            assert self.dialog._get_selected_encoding_row() == 0

        def test_editor_signals(self):

            self.dialog._undo_limit_radio.emit('toggled')
            self.dialog._undo_levels_spin.emit('value-changed')
            self.dialog._font_default_check.emit('toggled')
            self.dialog._font_button.emit('font-set')

        def test_file_signals(self):

            self.dialog._encoding_locale_check.emit('toggled')
            self.dialog._encoding_add_button.emit('clicked')
            selection =  self.dialog._encoding_view.get_selection()
            selection.unselect_all()
            selection.select_path(1)
            self.dialog._encoding_up_button.emit('clicked')
            selection.unselect_all()
            selection.select_path(0)
            self.dialog._encoding_down_button.emit('clicked')
            self.dialog._encoding_remove_button.emit('clicked')

        def test_preview_signals(self):

            self.dialog._preview_offset_spin.emit('value-changed')
            self.dialog._preview_select_radio.emit('toggled')
            self.dialog._preview_select_combo.emit('changed')
            self.dialog._preview_customize_button.emit('clicked')
            self.dialog._preview_command_entry.emit('changed')

    TestPreferencesDialog().run()
