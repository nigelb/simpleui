#!/usr/bin/env python

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

from distutils.core import setup

setup(name='simpleui',
    version='0.0.1',
    description='A Package implementing a number of simple UI patterns with fallback to CLI if the selected GUI fails.',
    author='NigelB',
    author_email='nigel.blair+simpleui@gmail.com',
    url='http://github.com/nigelb/simpleui',
    packages=['simpleui', 'simpleui.gtk_impl', 'simpleui.cli_impl'],
    package_dir={'simpleui.gtk_impl': 'simpleui/gtk_impl'},
    package_data={'simpleui.gtk_impl': ['ui/*.ui']},
    requires=["keyring"],
)

