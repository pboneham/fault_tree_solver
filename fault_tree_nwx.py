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

import networkx
import matplotlib.pyplot as plt
import itertools
import ft_import

def minimalise(ft):
    cs_tops = ft.successors("SOLUTION_TOP")
    combs = itertools.product(cs_tops, cs_tops)
    for comb in combs:
        if comb[0] == comb[1]:
            continue
        cs_entries0 = ft.successors(comb[0])
        cs_entries1 = ft.successors(comb[1])
        if len(cs_entries0) < len(cs_entries1):
            remove = 1
            for entry in cs_entries0:
                if entry not in cs_entries1:
                    remove = -1
                    break
        else:
            remove = 0
            for entry in cs_entries1:
                if entry not in cs_entries0:
                    remove = -1
                    break
        if remove == 0:
            try:
                ft.remove_edge("SOLUTION_TOP",comb[0])
            except:
                pass
        if remove == 1:
            try:
                ft.remove_edge("SOLUTION_TOP",comb[1])
            except:
                pass

def solve(ft):
    # identify top gate
    for node in networkx.nodes(ft):
        if ft.node[node]["top"] == 1:
            top = node
            break
    print top
    tmp = ft.node[top]["gtype"]
    solution_top = "SOLUTION_TOP"
    ft.add_node(solution_top, gtype="OR", module = "", top=2) # 2 means solution top
    ft.add_node("CS_TOP_1",gtype = "AND", module = "", top = 3) # 3 means it holds a cutset
    ft.add_edge(solution_top,"CS_TOP_1")
    ft.add_edge("CS_TOP_1", top)
    # now ready to start iterating
    counter = 1
    iter_count = 0
    while 1:
        cs_tops = ft.successors(solution_top)
        iter_count += 1
        print "Iter count", iter_count
        new_cs_tops = []
        gate_count = 0
        for cs_top in cs_tops:
            cs_entries = ft.successors(cs_top)
            for cs_entry in cs_entries:
                if ft.node[cs_entry]["gtype"] == "AND":
                    gate_count += 1
                    # need to disconnect the entry and connect its children
                    children = ft.successors(cs_entry)
                    for child in children:
                        ft.add_edge(cs_top, child)
                    ft.remove_edge(cs_top, cs_entry)
                if ft.node[cs_entry]["gtype"] == "OR":
                    gate_count += 1
                    # or gate leads to adding new cs_tops
                    children = ft.successors(cs_entry)
                    done_first = 0
                    for child in children:
                        if done_first == 0:
                            # add first child to current cs top
                            ft.add_edge(cs_top, child)
                            ft.remove_edge(cs_top, cs_entry)
                            done_first += 1
                        else:
                            # otherwise generate new tops
                            counter += 1
                            s = "CS_TOP_" + str(counter)
                            print "CS top to add:", s
                            tmp = [s]
                            tmp.append(child)
                            for tmp_entry in cs_entries:
                                if tmp_entry != cs_entry:
                                    tmp.append(tmp_entry)
                            new_cs_tops.append(tmp)
        # add extra nodes
        for entry in new_cs_tops:
            ft.add_node(entry[0])
            ft.add_edge(solution_top, entry[0])
            for cs_entry in entry[1:]:
                ft.add_edge(entry[0], cs_entry)
        minimalise(ft)
        print "Gate count =", gate_count
        if gate_count == 0: # this is how we get out!
            break
        

def createFT():
    ft = networkx.DiGraph()
    # create gates
    ft.add_node("G1", gtype = "AND", module="", top=1, ref_count = 0)
    ft.add_node("G2", gtype = "OR", module="", top=0, ref_count = 0)
    ft.add_node("G3", gtype = "AND", module="", top=0, ref_count = 0)
    #ft.add_node("G4", gtype = "OR", module="", top=0, ref_count = 0)
    #ft.add_node("G5", gtype = "OR", module="", top=0, ref_count = 0)
    # create BEs
    ft.add_node("BE1", gtype = "BE")
    ft.add_node("BE2", gtype = "BE")
    ft.add_node("BE3", gtype = "BE")
    ft.add_node("BE4", gtype = "BE")
    ft.add_node("BE5", gtype = "BE")
    ft.add_node("BE6", gtype = "BE")
    ft.add_node("BE7", gtype = "BE")
    # add inputs (add edges) - from (gate) to (input)
    ft.add_edge("G1","BE1")
    ft.add_edge("G1","G2")
    ft.add_edge("G2","BE2")
    ft.add_edge("G2","BE3")
    ft.add_edge("G2","G3")
    ft.add_edge("G3","BE3")
    ft.add_edge("G3","BE2")
    ft.add_edge("G3","BE4")
    #ft.add_edge("G4","BE4")
    #ft.add_edge("G4","BE6")
    #ft.add_edge("G4","BE7")
    #ft.add_edge("G5","BE5")
    #ft.add_edge("G5","BE2")
    for n in networkx.nodes(ft):
        ft.node[n]["ref_count"] = len(ft.predecessors(n))
        print n, ft.node[n]["ref_count"]
    return ft


################## tree class is used as interface to frontend  #####
class tree:

    def __init__(self):
        self.ft = createFT()
    ## end method ##


    def create_from_ft(self, f):
        pass

    def print_tree(self):
        #print networkx.info(ft)
        #print networkx.nodes(ft)

    # print out tree
        cs_tops = ft.successors("SOLUTION_TOP")
        for cs_top in cs_tops:
            print cs_top,
            cs_entries = ft.successors(cs_top)
            for entry in cs_entries:
                print entry,
            print

        networkx.draw(ft)
        plt.show()
    ## end method ##

    def print_gate(self, name=None):
        pass
    ## end method ##

    def solve(self, gate=None):
        solve(self.ft)
    ## end method ##
