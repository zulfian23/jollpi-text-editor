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

import gtksourceview2 as gtksourceview
import pango
import gtk

MARK_TYPE_1 = 'one'
MARK_TYPE_2 = 'two'

class Editor(gtksourceview.View):
	def __init__(self):
		gtksourceview.View.__init__(self)
		self.buffer = gtksourceview.Buffer()
		self.set_buffer(self.buffer)
		self.connect("key-release-event",self.on_key_release_event)
		self.connect("button-press-event", self.button_press)

		self.scheme = gtksourceview.style_scheme_manager_get_default()
		style = self.scheme.get_scheme("kate")
		
		self.buffer.set_style_scheme(style)

		font_desc = pango.FontDescription('monospace')
		if font_desc:
			font_desc.set_size(10 * pango.SCALE)
			self.modify_font(font_desc)
			
		try:
			pixbuf = gtk.gdk.pixbuf_new_from_file('/usr/share/pixmaps/apple-red.png')
		except:
			pixbuf = gtk.gdk.pixbuf_new_from_file('/usr/local/share/pixmaps/apple-red.png')

		if pixbuf:
			self.set_mark_category_pixbuf(MARK_TYPE_1, pixbuf)
			self.set_mark_category_priority(MARK_TYPE_1, 1)
			
		try:
			pixbuf1 = gtk.gdk.pixbuf_new_from_file('/usr/share/pixmaps/apple-green.png')
		except:
			pixbuf1 = gtk.gdk.pixbuf_new_from_file('/usr/local/share/pixmaps/apple-green.png')

		if pixbuf1:
			self.set_mark_category_pixbuf(MARK_TYPE_2, pixbuf1)
			self.set_mark_category_priority(MARK_TYPE_2, 2)
			
		self.set_wrap_mode(gtk.WRAP_NONE)
		self.set_highlight_current_line(1)

	def get_language_for_mime_type(self, mime):
		lang_manager = gtksourceview.language_manager_get_default()
		lang_ids = lang_manager.get_language_ids()
		for i in lang_ids:
			lang = lang_manager.get_language(i)
			for m in lang.get_mime_types():
				if m == mime:
					return lang
		return None
	
	def set_language(self, lang):
		self.buffer.set_language(lang)	
		self.buffer.set_highlight_syntax(1)
		self.buffer.set_highlight_matching_brackets(1)
			
	def on_key_release_event(self, widget, key):
		if key.keyval == 34:
			self.buffer.insert_at_cursor('"')
		elif key.keyval == 39:
			self.buffer.insert_at_cursor("'")
		elif key.keyval == 40:
			self.buffer.insert_at_cursor(")")
		elif key.keyval == 91:
			self.buffer.insert_at_cursor(']')
		elif key.keyval == 96:
			self.buffer.insert_at_cursor('`')
		elif key.keyval == 123:
			self.buffer.insert_at_cursor("}")
			
	def button_press(self, widget, event):
		if not self.get_show_line_marks():
			return 0
		
		if event.window == self.get_window(gtk.TEXT_WINDOW_LEFT):
			if event.button == 1:
				mark_type = MARK_TYPE_1
			else:
				mark_type = MARK_TYPE_2
				
			x_buf, y_buf = self.window_to_buffer_coords(gtk.TEXT_WINDOW_LEFT, int(event.x), int(event.y))
			line_start = self.get_line_at_y(y_buf)[0]
			mark_list = self.buffer.get_source_marks_at_line(line_start.get_line(), mark_type)
			
			if mark_list:
				self.buffer.delete_mark(mark_list[0])
			else:
				self.buffer.create_source_mark(None, mark_type, line_start)
				
		#return 0
		
	def _get_text(self):
		return self.buffer.get_text(self.buffer.get_start_iter(), self.buffer.get_end_iter())
	
	def _set_text(self, text):
		self.buffer.set_text(text)
		
	def _scroll_to_mark(self, mark):
		if mark:
			self.scroll_to_mark(self.buffer.get_selection_bound(), 0)
		else:
			self.scroll_to_mark(self.buffer.get_insert(), 0)
	
	#def _insert_text(self, text):
	#	self.buffer.insert(self.iter, text)
	
	def _undo(self):
		self.buffer.can_undo()
		self.buffer.undo()
		
	def _redo(self):
		self.buffer.can_redo()
		self.buffer.redo()
	
	def _cut(self):
		self.buffer.cut_clipboard(gtk.clipboard_get(), 1)
	
	def _copy(self):
		self.buffer.copy_clipboard(gtk.clipboard_get())

	def _paste(self):
		self.buffer.paste_clipboard(gtk.clipboard_get(),None, 1)
		
	def _select_all(self):
		self.buffer.select_range(self.buffer.get_start_iter(), self.buffer.get_end_iter())
		
	def _delete(self):
		self.buffer.delete_selection(0, 1)
	
	def _set_wrap_mode(self, val):
		if val == 1:
			self.set_wrap_mode(gtk.WRAP_NONE)
		elif val == 2:
			self.set_wrap_mode(gtk.WRAP_CHAR)
		else:
			self.set_wrap_mode(gtk.WRAP_WORD)
			
	def _set_scheme(self, val):
		if val == 1:
			style = self.scheme.get_scheme("kate")
		elif val == 2:
			style = self.scheme.get_scheme("classic")
		elif val == 3:
			style = self.scheme.get_scheme("tango")
		elif val == 4:
			style = self.scheme.get_scheme("oblivion")
		else:
			style = self.scheme.get_scheme("jollpi")
			
		self.buffer.set_style_scheme(style)
			
	def _set_auto_indent(self, val):
		self.set_auto_indent(val)
	
	def _set_show_line_numbers(self, val):
		self.set_show_line_numbers(val)
		
	def _set_show_line_marks(self, val):
		self.set_show_line_marks(val)
		
	def _set_show_right_margin(self, val):
		self.set_show_right_margin(val)
		
	def current_font(self):
		return self.get_pango_context().get_font_description().to_string()
	
	def set_font(self, font):
		font_desc = pango.FontDescription(font)
		if font_desc:
			self.modify_font(font_desc)
