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

ui_info = """
<ui>
	<toolbar name = "ToolBar">
		<toolitem action = "new"/>
		<toolitem action = "open"/>
		<separator/>
		<toolitem action = "save"/>
		<toolitem action = "save_as"/>
		<separator/>
		<toolitem action = "print"/>
		<separator/>
		<toolitem action = "undo"/>
		<toolitem action = "redo"/>
		<toolitem action = "cut"/>
		<toolitem action = "copy"/>
		<toolitem action = "paste"/>
		<separator/>
		<toolitem action = "find"/>
		<toolitem action = "replace"/>
	</toolbar>
</ui>
"""

class ToolBar(gtk.HandleBox):
	def __init__(self, menu):
		gtk.HandleBox.__init__(self)
		entries = [
			("new", gtk.STOCK_NEW, None, None, "Create a new file", self.do_new),
			("open", gtk.STOCK_OPEN, None, None, "Open a file", self.do_open),
			("save", gtk.STOCK_SAVE, None, None, "Save the current file", self.do_save),
			("save_as", gtk.STOCK_SAVE_AS, None, None, "Save the current file with a different name", self.do_save_as),
			("print", gtk.STOCK_PRINT, None, None, "Print the current page", self.do_print_page),
			("undo", gtk.STOCK_UNDO, None, None, "Undo the las editing command", self.do_undo),
			("redo", gtk.STOCK_REDO, None, None, "Redo the last undo step", self.do_redo),
			("cut", gtk.STOCK_CUT, None, None, "Cut selected text", self.do_cut),
			("copy", gtk.STOCK_COPY, None, None, "Copy selected text", self.do_copy),
			("paste", gtk.STOCK_PASTE, None, None, "Paste the clipboard", self.do_paste),
			("find", gtk.STOCK_FIND, None, None, "Search for text", self.do_find),
			("replace", gtk.STOCK_FIND_AND_REPLACE, None, None, "Search for and replace text", self.do_replace)
			]
		
		global menubar
		menubar = menu
		
		actions = gtk.ActionGroup("actions")
		actions.add_actions(entries)
		
		ui = gtk.UIManager()
		ui.insert_action_group(actions, 0)
		ui.add_ui_from_string(ui_info)
		toolbar = ui.get_widget("/ToolBar")
		toolbar.set_orientation(gtk.ORIENTATION_HORIZONTAL)
		toolbar.set_style(gtk.TOOLBAR_ICONS)
		
		self.undo = toolbar.get_nth_item(8)
		self.redo = toolbar.get_nth_item(9)
		self.cut = toolbar.get_nth_item(10)
		self.copy = toolbar.get_nth_item(11)
		self.undo.set_sensitive(0)
		self.redo.set_sensitive(0)
		self.cut.set_sensitive(0)
		self.copy.set_sensitive(0)
		
		self.add(toolbar)

		menubar.aneh(self.undo, self.redo, self.cut, self.copy)

	def do_new(self, widget):
		menubar.new(self)
	
	def do_open(self, widget):
		menubar.open(self)
	
	def do_save(self, widget):
		menubar.save_current_file(self)
		
	def do_save_as(self, widget):
		menubar.save_as(self)
		
	def do_print_page(self, widget):
		menubar.print_page(self)

	def do_undo(self, widget):
		menubar.undo(self)
		
	def do_redo(self, widget):
		menubar.redo(self)
		
	def do_cut(self, widget):
		menubar.cut(self)
		
	def do_copy(self, widget):
		menubar.copy(self)
	
	def do_paste(self, widget):
		menubar.paste(self)
		
	def do_find(self, widget):
		menubar.find(self)
		
	def do_replace(self, widget):
		menubar.replace(self)