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

ui_impl = None
default_ui_precedence = ["gtk", "cli"]

def require(impl="gtk", ui_precedence=default_ui_precedence):
    global ui_impl
    found = False
    for i in ui_precedence:
        if i == impl:
            found = True
            try:
                a = __import__("simpleui.%s_impl.impl"% i).__dict__["%s_impl"% i]
                if a.COMMONUI_AVAILABLE:
                    ui_impl = a.simpleui_Impl
                    return
            except Exception, t:
                print t
                pass
        elif found:
            try:
                a = __import__("simpleui.%s_impl.impl"% i).__dict__["%s_impl"% i]
                print a, a.COMMONUI_AVAILABLE, a.simpleui_Impl
                if a.COMMONUI_AVAILABLE:
                    ui_impl = a.simpleui_Impl
                    print i
                    return
            except:
                pass


def __test_type(value):
    v = value.lower()
    if v in ["true", "yes", "y"]:
        return True
    return False


def __add_args(parser, default_ui="gtk", default_use_keyring=True):
    parser.add_argument("-u", "--use-ui", dest="ui_impl", help="Force the use of the specified ui implementation.", default="gtk", metavar="UI_NAME")
    parser.add_argument("-k", "--use-keyring", dest="use_keyring", default=True, type=__test_type, help="Use the systems Keyring")



def setup_parser(parser, config):
    if config.read_config():
        __add_args(parser, default_ui=config.get('ui_impl'), default_use_keyring=config.get("use_keyring"))
    else:
        __add_args(parser)

def create_UI(namespace, config, raise_cancelled=False):
    if not config.read_config():
        config.initialize_dir(namespace)
    require(config.get("ui_impl"))
    from simpleui.impl import simpleui_impl
    return simpleui_impl(config, raise_cancelled=raise_cancelled)
