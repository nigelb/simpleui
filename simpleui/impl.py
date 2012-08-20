# simpleui implements a number of simple UI patterns with fallback to CLI if the
# selected GUI fails.
#
# Copyright (C) 2012 NigelB
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

from simpleui import ui_impl
from simpleui.exceptions import Cancelled
from simpleui.utils import FileSelectorTypes
try:
    import keyring
except: pass

import keyring

def test_cancelled(fn):
    def func(self, *args, **kwargs):
        result = fn(self, *args, **kwargs)
        if result is None and self.rc:
            raise Cancelled()
        return result
    return func



class simpleui_impl:
    def __init__(self, config, raise_cancelled=False):
        self.ui = ui_impl()
        self.config = config
        self.rc = raise_cancelled

    def get_credentials(self, bad_credential=False, service="Test", uname=None):
        if uname is None and self.config.has_key("username"):
            uname = self.config.get("username")
        if self.config.get("use_keyring"):
            if (not bad_credential) and uname is not None:
                return (uname, keyring.get_password(service, uname))
            else:
                ok, username, password = self.ui.prompt_credentials(service)
                if ok:
                    keyring.set_password(service, username, password)
                    self.config.set("username",username)
                    self.config.write_config()
                    return (username, password)
                return (None, None)
        else:
            ok, username, password = self.ui.prompt_credentials()
            if ok:
                return  (username, password)
            return (None, None)

    @test_cancelled
    def prompt_list(self, title, message, model, multi_select=False):

        return self.ui.prompt_list(title, message, model, multi_select=multi_select)

    @test_cancelled
    def prompt_file_selector(self, title="Enter the filename:", start_dir=".", type=FileSelectorTypes.SAVE):
        return self.ui.prompt_file_selector(title=title, start_dir=start_dir, type=type)


    def display_graph(self, title="Graph", graph=None):
        return self.ui.display_graph(title=title, graph=graph)

    def prompt_yes_no(self, message):
        return self.ui.prompt_yes_no(message)


    def get_list_model(self):
        return []

