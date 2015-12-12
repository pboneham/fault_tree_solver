#################################################################################
#    This file is a simple gui frontend for testing (and possibly using) the
#    ftsolver module. It was developed by Paul S. Boneham
#    Copyright (C) 2015  Paul S. Boneham
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

import wx
import ft

CONFIG_TREE_TO_SOLVE = "./example.ft"

class ftgui(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, -1, title)

        filemenu= wx.Menu()
        filemenu.Append(100,"E&xit"," Exit, bye")
        filemenu.Append(200,"R&un"," Run - solve FT")
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File")
        self.SetMenuBar(menuBar)

        # bind events to functions
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_MENU, self.OnExit, id=100)
        self.Bind(wx.EVT_MENU, self.solveTree, id=200)

        self.sb = self.CreateStatusBar()
        size = wx.Size(300,200)
        self.SetSize(size)
        self.Center()
        self.Show(True)

    def solveTree(self, event):
        refvalue = 5
        prg = wx.ProgressDialog("FT solver", "Progress", refvalue, style=wx.PD_CAN_ABORT)
        completed = 0
        try:
            t = ft.tree()
            prg.Update(1)
            print "create tree from SETS file"
            t.create_from_ft(CONFIG_TREE_TO_SOLVE)
            #t.print_tree()
            prg.Update(2)
            print "prepare tree (check multiple refs)"
            t.prepare()
            prg.Update(3)
            print "Solve tree ..."
            t.solve()
            prg.Update(4)
            t.print_gate()
            prg.Update(5)
            completed = 1
        except:
            pass
        if completed == 1:
            print "completed OK"
            prg.Update(5, newmsg = "Success")
        else:
            print "error occurred"
            prg.Update(5, newmsg = "There was an error")
        prg.Destroy()

    def OnSize(self, event):
        size = self.GetSize()
        event.Skip()

    def OnExit(self,e):
        self.Close(True)

app = wx.App(True) # True - redirect standard out & error, user can see prints
ftgui(None, -1, 'FT solver simple GUI - for testing ft module')

app.MainLoop()
