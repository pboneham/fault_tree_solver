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
class base_filter:

    def __init__(self, infile):
        self.infile = infile
        self.events = {}
        pass

    def load_file(self,fn):
        self.f = open(fn,"r")
        pass

    def export_tree(self):
        f.close()
        return self.events

class sets_filter(base_filter):

    def __init__(self, infile):
        super(sets_filter,self).__init__(self, infile)


    def load_file(self, f):
        # import a SETs file into the self.events structure
        fs = open(f,"r")
        print "Opened file"
        counter = 0
        while 1:
            line = fs.readline()
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
        fs.close()
    ## end method ##


class ft_filter(base_filter):

    def __init__(self, infile):
        super(sets_filter,self).__init__(self, infile)


    def load_file(self, f):
        # import a ft file into the self.events structure
        fp = open(fp,"r")
        cp = ConfigParser.ConfigParser()
        cp.readfp(fp)
        counter = 0
        # now get settings, tree and data
        # settings
        top = cp.get("control","top")
        cutoff = cp.get("control", "cutoff")
        #tree
        tree_entries = cp.items("tree")
        for item in tree_entries:
            self.events[item[0]] = gate_inputs()
            gate_in_items = item[1].split(",")
            if gate_in_items[0].upper() == "OR":
                for it in gate_in_items[1:]:
                    self.events[item[0]].add_row([it])
            if gate_in_items[0].upper() == "AND":
                for it in gate_in_items[1:]:
                    tmp.append(it)
            self.events[item[0]].add_row(tmp)
        #data
        data_entries = cp.items("data")
        for item in data_entries:
            self.events[item[0]] = float(item[1])
        
    ## end method ##



################## Gate Inputs Class ###################################
class gate_inputs:

    def __init__(self):
        self.inputs = [] # no inputs
        self.nrefs = 0
        self.name = ""
        self.current_offsets = [-1,-1]
        self.solved = 0 # not solved, 1 indicates solved
        self.inputs_recursive_count = 0
        self.input_be_recursive_count = 0
    ## end method ##


    def next_in_row(self):
        self.current_offsets[1] = self.current_offsets[1] + 1
        if self.current_offsets[1]  >= len(self.inputs[ self.current_offsets[0] ]) or self.current_offsets[0] == -1:
            self.current_offsets[0] = self.current_offsets[0] + 1
            self.current_offsets[1] = 0
        if self.current_offsets[0] + 1 > len(self.inputs): # past last element of last row
            self.current_offsets[0] = -1
            self.current_offsets[1] = -1
            return self.current_offsets[0], self.current_offsets[1]
        return self.current_offsets[0], self.current_offsets[1]
    ## end method ##


    def add_row(self, fields):
        tmp = []
        for item in fields:
            tmp.append(item)
        self.inputs.append(tmp)
    ## end method ##


    def remove_row(self, offset):
        del self.inputs[offset]
        # reset positions
        if self.current_offsets[0] > offset:
            self.current_offsets[0] = self.current_offsets[0] - 1
    ## end method ##


    def remove_from_row(self, row_offset, col_offset):
        del self.inputs[row_offset][col_offset]
        self.current_offsets[1] = self.current_offsets[1] - 1
        if self.current_offsets[1] == -1:
            self.current_offsets[0] = self.current_offsets[0] - 1
            self.current_offsets[1] = len( self.inputs[ self.current_offsets[0] ] ) - 1
    ## end method ##


    def clone(self, offset):
        result = []
        for item in self.inputs[offset]:
            result.append(item)
        return result
    ## end method ##


    def minimalise(self):
        # reset position to start
        self.current_offsets = [-1,-1]
        self.inputs.sort(cmp = by_length)
        row = 0
        end_row = len(self.inputs) - 1
        while 1:
            inner_row = row + 1
            while 1:
                if inner_row > end_row:
                    break
                first = self.inputs[row]
                second = self.inputs[inner_row]
                if compare_cutsets(first, second) == 1:
                    del self.inputs[inner_row]
                    end_row = end_row - 1
                    continue
                else:
                    inner_row = inner_row + 1
            row = row + 1
            if row > end_row:
                break
        #for r in self.inputs:
        #   for item in r:
        #       print item,
        #   print


####################Tree Class #########################################
class tree:

    def __init__(self):
        self.events = {}
        self.cutoff = 0.0
        self.tops =[]
        self.cur_top = 0
    ## end method ##


    def create_from_ft(self, f):
        tmp = ft_filter()
        tmp.load_file(f)
        self.events = tmp.export_tree()
        

    def print_tree(self):
        for key in self.events.keys():
            print key, 
            self.print_gate(key)
    ## end method ##


    def print_gate(self, name=None):
        if name == None:
            name = self.tops[self.cur_top]
        try:
            x = self.events[name] * 1
            print "(Basic Event):  ", self.events[name]
            return
        except:
            pass
        rows = self.events[name].inputs
        print "Number of cutsets generated = ", len( self.events[name].inputs )
        print "(Gate): "
        for row in rows:
            for item in row:
                print "  ", item,
            print ""
    ## end method ##


    def solve(self, gate=None):
        if gate == None:
            gate = self.tops[cur_top]
        solution = self.events[gate]
        r_prev = -1
        last_minimalisation = 0
        while 1: # iterate along and over rows
            # so we are selecting an input
            # and dealing with this
            # then we'll go round again
            # just so long as we add any new rows
            # at the end and new events at the current
            # row end we should be OK
            r,c = solution.next_in_row()
            if r == -1:
                break # this should get us out when finished since we will
                      # move on over BEs that are pulled in (see try/except below)
            if r != r_prev:
                print "---- On row:", r+1, " / ", len( solution.inputs )
                r_prev = r
            if len(solution.inputs) > (5000 + last_minimalisation) * 1.2: # point at which we minimalise - could be tweaked
                print "Minimalise solution"
                solution.minimalise()
                last_minimalisation = len(solution.inputs)
                continue
            # find input gate or be
            in_node_name = solution.inputs[r][c]
            in_node = self.events[in_node_name]
            try:
                x = in_node * 1
            except:
                if in_node.nrefs > 1 and in_node.solved == 0:
                    # solve multiply referenced node before continuing
                    print "Solve multiple referenced gate", in_node_name
                    self.solve(in_node_name)
                    print "-- solved"
                # really is a gate
                # FIRST: count the rows in the input
                nrows = len(in_node.inputs)
                icounter = 0
                solution.remove_from_row(r,c)
                reference_row = solution.clone(r)
                # before expanding the rows we should update the reference
                # counts on the fault tree gates, otherwise we may end up solving 
                # multiple times
                for item_name in reference_row:
                    try:
                        x = self.events[item_name]
                    except:
                        self.events[item_name].nrefs = self.events[item_name].nrefs + nrows - 1
                while icounter < nrows:
                    if icounter > 0:
                        current_row = copy.copy(reference_row)
                        solution.inputs.append(current_row)
                    else:
                        current_row = solution.inputs[r]
                    for item in in_node.inputs[icounter]:
                        if item not in current_row:
                            current_row.append(item)
                    icounter = icounter + 1
        self.events[gate].minimalise()
        self.events[gate].solved = 1
    ## end method ##


    def prepare(self):
        # this method will identify multiply referenced gates
        # it will also mark modules and count
        # inputs recursively as well as distinct BE
        # count (recursively)
        references = {}
        keys = self.events.keys()
        for key in keys:
            node = self.events[key]
            try:
                x = node * 1
            except:
                # must be a gate, so set up entry in references
                references[key] = 0
        keys = references.keys()
        for key in keys:
            # iterating over gates only
            rows = self.events[key].inputs
            for row in rows:
                for item in row:
                    try:
                        x = self.events[item] * 1
                    except:
                        # gate so increment ref
                        references[item] = references[item] + 1
        for key in keys:
            self.events[key].nrefs = references[key]
            self.events[key].name = key
            #print key, references[key]

    ## end method ##
        
        
########################################################################


################ Functions #############################################
def by_length(first, second):
    return len(first) - len(second)


def compare_cutsets(shorter, longer):
    result = 1
    for item in shorter:
        if item not in longer:
            return 0
    return result

########################################################################
