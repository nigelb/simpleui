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

import getpass

class cli_impl:
    ui_type = "cli_impl"

    def prompt_credentials(self, service):
        print "Please enter you your Credentials for %s: "%service
        username = raw_input("Username: ")
        password = getpass.getpass("Password: ")
        return (True, username, password)

    def prompt_file_selector(self, title="Enter the filename:", start_dir=".", type=""):
        return [raw_input(title)]

    def prompt_yes_no(self, message):
        input = raw_input("%s [Y/N]: "%message)
        if not len(input): return self.prompt_yes_no(message)
        try:
            return {"Y":True,"N":false}[input[0].upper()]
        except Exception as e:
            return self.prompt_yes_no(message)

    def prompt_list(self, title, prompt, data, multi_select=False):
        print(title)
        for item in range(len(data)):
            print ("\t%i. %s"%(item,data[item]))
        toRet = []
        if multi_select is False:
            return [int(raw_input(prompt))]
        else:
            print ()
            print ('Enter as many as required then enter "f" to finish.')
            print ()
            try:
                while True:
                    toRet.append(int(raw_input("%s "%prompt)))

            except ValueError as v:
                pass
        print ()
        return toRet


