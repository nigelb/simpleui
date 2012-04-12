# simpleui implements a number of simple UI patterns with fallback to CLI if the
# selected GUI fails.
#
# Copyright (C) 2011 NigelB
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

from gRefer.ui.chooser_types import FileSelectorTypes


try:
    import pygtk

    pygtk.require("2.0")
except:
    pass

import gtk, gobject
import gtk.glade
import os

from gtk import gdk

__ui_path = os.path.join(os.path.dirname(__file__), 'ui')

class creds_model:
    def __init__(self, builder, title):
        self.window = builder.get_object("CredentialsDialog")
        self.window.set_title(title)
#        self.window.set_default_size(450,-1)
        self.ok = False
        self.username = None
        self.password = None
        self._username = builder.get_object("username")
        self._password = builder.get_object("password")
        builder.connect_signals(self)

    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()


    def on_ok_clicked(self, widget, data=None):
        self.ok = True
        self.username = self._username.get_text()
        self.password = self._password.get_text()
        gtk.main_quit()


    def on_cancel_clicked(self, widget, data=None):
        gtk.main_quit()


    def get_creds(self):
        self.window.show()
        gtk.main()
        return (self.ok, self.username, self.password)

    def on_key_press(self, widget, event, data=None):
        kp = gdk.keyval_name(event.keyval)
        if kp == "Return" or kp == "KP_Enter":
            self.on_ok_clicked(widget)


class prompt_list_model:
    def __init__(self, builder, title, prompt, multi_select=False):
        self.window = builder.get_object("TreeViewSelector")
        self.window.set_title(title)
        self.selected_value = None

        self._prompt = builder.get_object("TVS_LABEL")
        self._prompt.set_text(prompt)

        self._treeview = builder.get_object("TVS_Tree")
        if multi_select:
            self._treeview.get_selection().set_mode(gtk.SELECTION_MULTIPLE)
        builder.connect_signals(self)
        self.tvcolumn = gtk.TreeViewColumn("")
        self._treeview.append_column(self.tvcolumn)
        self.cell = gtk.CellRendererText()
        self.tvcolumn.pack_start(self.cell, True)
        self.tvcolumn.add_attribute(self.cell, 'text', 0)

        #		self.window.set_geometry_hints(
        #			geometry_widget,
        #			min_width=-1,
        #			min_height=-1,
        #			max_width=-1,
        #			max_height=-1,
        #			base_width=-1,
        #			base_height=-1,
        #			width_inc=-1,
        #			height_inc=-1,
        #			min_aspect=-1.0,
        #			max_aspect=-1.0
        #		)
        self.window.resize(400, 300)


    def get_selection(self):
        self.window.show()
        gtk.main()
        return self.selected_value

    def on_cancel_clicked(self, widget, data=None):
        self.window.hide()
        gtk.main_quit()

    def on_ok_clicked(self, widget, data=None):
        self.selected_value = [x[0] for x in self._treeview.get_selection().get_selected_rows()[1]]
        self.window.hide()
        gtk.main_quit()

    def insert_list_data(self, data):
        model = None
        model = gtk.ListStore(gobject.TYPE_STRING)
        p = None
        for i in data:
            model.append([i])
        self._treeview.set_model(model=model)

    def insert_data(self, data):
        if isinstance(data, list):
            self.insert_list_data(data)

    def on_key_press(self, widget, event, data=None):
        kp = gdk.keyval_name(event.keyval)
        if kp == "Return" or kp == "KP_Enter":
            self.on_ok_clicked(widget)

class file_model:
    def __init__(self, builder):
        self.window = builder.get_object("FileChooser")
        self.selected_value = None
        builder.connect_signals(self)

    def get_filename(self, title="Select File/Folder",start_dir=".", action=gtk.FILE_CHOOSER_ACTION_OPEN):
        self.window.set_title(title)
        self.window.set_current_folder(start_dir)
        self.window.set_action(action)
        self.window.show()
        gtk.main()
        return self.selected_value

    def on_file_selected(self, widget, data=None):
        self.selected_value = self.window.get_filenames()
        if self.selected_value is None:
            self.selected_value = [self.window.get_filename()]
        self.window.hide()
        gtk.main_quit()

    def on_key_press(self, widget, event, data=None):
        kp = gdk.keyval_name(event.keyval)
        if kp == "Return" or kp == "KP_Enter":
            self.on_file_selected(widget)

    def on_cancel_clicked(self, widget, data=None):
        self.window.hide()
        gtk.main_quit()

class gtk_impl:
    ui_type = "gtk_impl"

    def __init__(self):
        self.ui_path = os.path.join(os.path.dirname(__file__), "ui/")
        self.types={
            FileSelectorTypes.OPEN:gtk.FILE_CHOOSER_ACTION_OPEN,
            FileSelectorTypes.SAVE:gtk.FILE_CHOOSER_ACTION_SAVE,
            FileSelectorTypes.SELECT_FOLDER:gtk.FILE_CHOOSER_ACTION_SELECT_FOLDER,
            FileSelectorTypes.CREATE_FOLDER:gtk.FILE_CHOOSER_ACTION_CREATE_FOLDER,
        }

    def __create_builder(self, ui_file):
        builder = gtk.Builder()
        builder.add_from_file(ui_file)
        return builder


    def __create_ui_path(self, name):
        return os.path.join(self.ui_path, name)

    def prompt_credentials(self, service):
        model = creds_model(self.__create_builder(self.__create_ui_path("Credentials.ui")), "Please enter your Credentials for %s: "%service)
        return model.get_creds()

    def prompt_file_selector(self, title="", start_dir=".", type=FileSelectorTypes.OPEN):
        model = file_model(self.__create_builder(self.__create_ui_path("FileChooser.ui")))
        return model.get_filename(title=title, start_dir=start_dir, action=self.types[type])

    def prompt_test_input(self):
        pass

    def prompt_yes_no(self, message):
        dlg = gtk.MessageDialog(buttons=gtk.BUTTONS_YES_NO, message_format=message)
        toRet = {gtk.RESPONSE_NO: False, gtk.RESPONSE_YES: True}[dlg.run()]
        dlg.hide()
        return toRet


    def prompt_list(self, title, prompt, data, multi_select=False):
        model = prompt_list_model(self.__create_builder(self.__create_ui_path("TreeListView.ui")), title, prompt,
                                  multi_select=multi_select)
        model.insert_data(data)
        return model.get_selection()

if __name__ == "__main__":
    gtk_impl().prompt_credentials()


