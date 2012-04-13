#!/usr/bin/env python

# CommonUI implements a number of common UI patterns with fallback to CLI if the
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

import simpleui
from argparse import ArgumentParser
from simpleui.utils import UserConfig


def setup_parser(parser): pass
def defaults(config, namespace): pass

if __name__ == '__main__':
    cfg = UserConfig(def_config_callback=defaults)
    parser = ArgumentParser()
    CommonUI.setup_parser(parser, cfg)
    setup_parser(parser)
    ui = simpleui.create_UI(parser.parse_args(), cfg)
