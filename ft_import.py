#################################################################################
#    This file is the ftsolver module, which solves fault trees.
#    It was developed by Paul S. Boneham. Copyright (C) 2015  Paul S. Boneham
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
##################################################################################

import string
import copy
import ConfigParser

########################################################################
################## Classes #############################################

################## FT file import filters ##############################
class base_filter(object):

    def __init__(self):
        self.events = {}
        self.tops = []
        self.cutoff = 0.0
        pass

    def load_file(self,fn):
        self.f = open(fn,"r")
        pass

    def export_tree(self):
        self.f.close()
        return self.events, self.tops, self.cutoff

class sets_filter(base_filter):

    def __init__(self):
        super(sets_filter,self).__init__()

    def load_file(self, f):
        # import a SETs file into the self.events structure
        super(sets_filter,self).load_file(f)
        counter = 0
        while 1:
            line = self.f.readline()
            if line == "":
                break
            line = string.replace(line, "\n", "")
            print line
            fields = string.split( line )
            if fields[0] == "AG$":
                ename = string.replace( fields[1], ".", "")
                self.events[ename] = gate_inputs()
                inputs = []
                for input in fields[3:]:
                    s = string.replace(input, ",", "")
                    s = string.replace(s, ".", "")
                    inputs.append(s)
                self.events[ename].add_row( inputs )
                print "done AND gate"
            if fields[0] == "OG$":
                ename = string.replace( fields[1], ".", "")
                self.events[ename] = gate_inputs()
                for input in fields[3:]:
                    inputs = []
                    s = string.replace(input, ",", "")
                    s = string.replace(s, ".", "")
                    inputs.append(s)
                    self.events[ename].add_row(inputs)
                print "done OR gate"
            if fields[0] == "BE$":
                ename = string.replace( fields[1], ".", "")
                self.events[ename] = 0.01
            if fields[0] == "IE$":
                ename = string.replace( fields[1], ".", "")
                self.events[ename] = 0.01
            print "Read line", counter
            counter += 1
        return super(sets_filter,self).export_tree()
    ## end method ##


class ft_filter(base_filter):

    def __init__(self):
        super(ft_filter,self).__init__()

    def load_file(self, f):
        # import a ft file into the self.events structure
        super(ft_filter,self).load_file(f)
        cp = ConfigParser.ConfigParser()
        cp.readfp(self.f)
        counter = 0
        # now get settings, tree and data
        # settings
        tmp = cp.get("control","evaluate")
        tmp = tmp.split(",")
        for item in tmp:
            self.tops.append(item.upper())
        cutoff = cp.get("control", "cutoff")
        #tree
        tree_entries = cp.items("tree")
        for item in tree_entries:
            entry_name = item[0].upper()
            self.events[entry_name] = gate_inputs()
            gate_in_items = item[1].split(",")
            if gate_in_items[0].upper() == "OR":
                print entry_name, "OR"
                for it in gate_in_items[1:]:
                    self.events[entry_name].add_row([it.upper()])
            if gate_in_items[0].upper() == "AND":
                print entry_name, "AND"
                tmp = []
                for it in gate_in_items[1:]:
                    tmp.append(it.upper())
                self.events[entry_name].add_row(gate_in_items[1:])
        #data
        data_entries = cp.items("data")
        for item in data_entries:
            entry_name = item[0].upper()
            self.events[entry_name] = float(item[1])
        return super(ft_filter,self).export_tree()
    ## end method ##
