#!/usr/bin/python

# Copyright (c) 2010 Zulfian 
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

class StatusBar(gtk.Statusbar):
	def __init__(self):
		gtk.Statusbar.__init__(self)
		self.ci = self.get_context_id("Status Bar")
		self.set_has_resize_grip(0)
		
	def show_status(self, message):
		self.push(self.ci, "%s" % message)
		
	def clear(self):
		self.push(self.ci, "")
		
class StatusBar1(StatusBar):
	def __init__(self):
		gtk.Statusbar.__init__(self)
		self.set_has_resize_grip(0)
		self.set_size_request(200, -1)
		self.ci = self.get_context_id("Status Bar1")
		row = 1
		col = 1
		i = 0		
		self.push(self.ci, "Line: %d, Col: %d" % (row, col))

	def show_line_col(self, buff):
		iter = buff.get_iter_at_mark(buff.get_insert())
		row = iter.get_line() + 1
		col = iter.get_line_offset() + 1
		self.push(self.ci, "Line: %d, Col: %d" % (row, col))

class StatusBar2(StatusBar1):
	def __init__(self):
		gtk.Statusbar.__init__(self)
		self.ci = self.get_context_id("Status Bar2")
		self.set_size_request(100, -1)
		self.push(self.ci, "INS")
		
	def change_overwrite(self, editor):
		if editor.get_overwrite():
			self.push(self.ci, "OVR")
		else:
			self.push(self.ci, "INS")
