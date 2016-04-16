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
import ft_zero
import fault_tree_nwx


################## dummy class linking to actual solver (there is a choice) #####
class tree:

    def __init__(self, use_nwx = int 0):
		if use_nwx == 0:
			self.ft_obj = ft_zero.tree()
		if use_nwx == 1:
			self.ft_o
		print "Fault tree object not created - index", use_nwx, "not available"
		exit(1)
    ## end method ##

    def create_from_ft(self, f):
        self.ft_obj.create_from_ft(f)

    def print_tree(self):
        self.ft_obj.print_tree(f)
    ## end method ##

    def print_gate(self, name=None):
		self.ft_obj.print_gate(name)
    ## end method ##

    def solve(self, gate=None):
    ## end method ##
