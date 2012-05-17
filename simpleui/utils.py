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
from StringIO import StringIO
import json

import os
from pprint import pprint
import simpleui


class FileSelectorTypes:
    OPEN = "OPEN"
    SAVE = "SAVE"
    SELECT_FOLDER = "SELECT_FOLDER"
    CREATE_FOLDER = "CREATE_FOLDER"


def ui_defaults(namespace):
    return {
        "ui_impl": namespace.ui_impl,
        "use_keyring": namespace.use_keyring,
        }

def serialize_objs(obj):
    return json.dumps(obj)

def serialize_obj(obj, fp):
    return json.dump(obj, fp)

def un_serialize_obj(file_handle):
    return json.load(file_handle)

def un_serialize_objs(to_un_serialize):
    return json.loads(to_un_serialize)


class config_helper:

    def __init__(self, config):
        self.config = config

    def __setattr__(self, key, value):
        if key == "config":
            self.__dict__[key] = value
        else:
            self.config[key] = value

    def __getitem__(self, item):
        return self.config[item]

    def __getattr__(self, key):
        if key is "__str__":            return self.config.__str__
        elif key is "__repr__":         return self.config.__repr__
        elif key is "__iter__":         return self.config.__iter__
        elif key is "config_delegate":  return self.config
        return self.config[key]

    def __contains__(self, item):
        return self.__getattr__(item)


class UserConfig:
    def __init__(self, dir_name=os.path.join(os.path.expanduser("~"), ".common_ui"), config_file="ui.config",
                 def_config_callback=ui_defaults, ui_precedence=simpleui.default_ui_precedence, write_on_initialize=True):
        self.config = None
        self.dir_name = dir_name
        self.config_file = os.path.join(dir_name, config_file)

        self.defaults_callback = def_config_callback
        self.ui_precedence = ui_precedence
        self.write_on_initialize = write_on_initialize

    def initialize_dir(self, namespace):
        if not os.path.exists(self.dir_name):
            os.mkdir(self.dir_name)
        if not os.path.exists(self.config_file):
            self.config = self.defaults_callback(namespace)
            if self.write_on_initialize:
                self.write_config()

    def write_config(self):
        cf = open(self.config_file, "wb")
        serialize_obj(self.config, cf)
        cf.close()


    def read_config(self):
        if not self.config is None:
            return True
        if os.path.exists(self.config_file):
            cf = open(self.config_file, "rb")
            self.config = un_serialize_obj(cf)
            cf.close()
            return True
        else:
            return False

    def get(self, key):
        return self.config[key]

    __getitem__ = get

    def set(self, key, value):
        self.config[key] = value

    __setitem__ = set

    def has_key(self, key):
        return self.config.has_key(key)

    def delete(self, key):
        del self.config[key]

    __delitem__ = delete

    def items(self):
        return self.config.items()

    def __iter__(self):
        return self.config.__iter__()

    def next(self):
        return self.config.next()

    def __repr__(self):
        return self.config.__repr__()