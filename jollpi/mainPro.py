#!/usr/bin/python

# Copyright (c) 2010 Zulfian <fianmyung@gmail.com>

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import gtk
import os
import sys

import MainEditor.menubar as menubar
import MainEditor.toolbar as toolbar
import MainEditor.notebook as notebook
import MainEditor.editor as editor
import MainEditor.statusbar as status

class MainWindow(gtk.Window):
	def __init__(self):
		gtk.Window.__init__(self)
		try:
			self.set_screen(parent.get_screen())
		except:
			self.connect("delete-event", self.close)
		
		self.set_default_size(600, 600)
		self.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.maximize()
		try:
			self.set_icon_from_file('/usr/share/pixmaps/jollpi.png')
		except:
			self.set_icon_from_file('/usr/local/share/pixmaps/jollpi.png')
		
		global ed
		global menubar
		global toolbar
		global statusbar
		global statusbar1
		global statusbar2
		global nb
		statusbar = status.StatusBar()
		statusbar1 = status.StatusBar1()
		statusbar2 = status.StatusBar2()
		ed = editor.Editor()
		nb = notebook.Notebook(self, statusbar)
		#nb.new_tab("Untitled")
		menubar = menubar.MenuBar(self, ed, statusbar, statusbar1, statusbar2, nb)
		menu = menubar.create_menu(self)
		toolbar = toolbar.ToolBar(menubar)
		
		box = gtk.VBox()
		box1 = gtk.HBox()

		box1.pack_start(statusbar, 1)
		box1.pack_start(statusbar1, 0)
		box1.pack_start(statusbar2, 0)
		box.pack_start(menu, 0)
		box.pack_start(toolbar, 0)
		box.pack_start(nb, 1)
		box.pack_start(box1, 0)
		self.add(box)
		
		if len(sys.argv) > 1:
			for x in sys.argv:
				print os.path.basename(x)
				if os.path.basename(x) == "jollpi":
					continue
				else:
					filename = x
					if os.path.exists(filename):
						menubar.open_file(filename, 1)
		else:
			nb.new_tab("Untitled")
	
	def close(self, widget, event, data = None):
		if menubar.quit(self):
			pass
		else:
			return 1