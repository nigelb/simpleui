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


COMMONUI_AVAILABLE = False
try:
    import pygtk
    pygtk.require("2.0")

except:
    pass
try:
    import gtk
    import gtk.glade

    gtk._gtk.init_check()
    COMMONUI_AVAILABLE = True
    from impl import gtk_impl as simpleui_Impl
except:
    print("GTK Not Availible")

__all__ = ["COMMONUI_AVAILABLE", "simpleui_Impl"]

