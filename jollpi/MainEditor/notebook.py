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
import os
import gobject
import editor as editor

try:
	import hashlib
except ImportError:
	import md5

try:
	import gio
	using_gio = 1
	using_gnomevfs = 0
except ImportError:
	import gnomevfs
	using_gio = 0
	using_gnomevfs = 1

class Notebook(gtk.Notebook):
	editor_instance = {}
	file = {}
	so = {}
	unsave = {}
	md5 = {}
	def __init__(self, window, st):
		gtk.Notebook.__init__(self)
		self.set_show_tabs(1)
		self.set_scrollable(1)
		self.set_tab_pos(gtk.POS_TOP)
		self.prnt = window
		self.status = st
		global ed
		ed = editor.Editor()
	
	def error_message(self, title, message, parent, sec_message = ""):
		msg = gtk.MessageDialog(parent, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
		msg.set_title(title)
		msg.format_secondary_text(sec_message)
		msg.run()
		msg.destroy()
		
	def info_message(self, title, message, parent):
		msg = gtk.MessageDialog(parent, 0, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, message)
		msg.set_title(title)
		msg.format_secondary_text("")
		msg.run()
		msg.destroy()
		
	def reset_status(self, key):
		name_of_file = None
		if len(self.file) != 0:
			name_of_file = self.file[key]
			self.prnt.set_title("%s - JOLLPI" % os.path.basename(name_of_file))
		else:
			self.prnt.set_title("Untitled - JOLLPI")
			
		return name_of_file
		
	def md5checksum(self, read):
		try:
			return hashlib.md5(read).hexdigest()
		except:
			return md5.new(read).hexdigest()

	def timer_id(self):
		gobject.timeout_add(3000, self.clear)
		
	def clear(self):
		self.status.clear()
		return 0
	
	def set_label(self, lbl, scrl, number, tip = None):
		label = self.create_tab_label(lbl, scrl, number, tip)
		self.set_tab_label(self.get_nth_page(self.get_current_page()), label)
		label.show_all()
		self.show_all()
		
	def get_label(self):
		hbox = self.get_tab_label(self.get_nth_page(self.get_current_page()))
		label_of_tab = hbox.get_children()
		text_of_tab = label_of_tab[1].get_text()
		return text_of_tab
	
	def get_values(self, child):
		key = None
		data = None
		i = 0
		for x in self.editor_instance:
			if child.get_children()[0] == self.editor_instance.values()[i]:
				key = self.editor_instance.keys()[i]
				data = self.editor_instance.values()[i]
			i = i + 1
		
		return key, data

	def new_tab(self, lbl):
		data = None
		self.editor = editor.Editor()
		scroll = gtk.ScrolledWindow()
		scroll.set_policy(hscrollbar_policy = gtk.POLICY_AUTOMATIC, vscrollbar_policy = gtk.POLICY_ALWAYS)
		scroll.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		scroll.add(self.editor)
		self.append_page(scroll)
		if len(self.editor_instance) == 0:
			data = self.page_num(scroll)
		else:
			i = 0
			for x in self.editor_instance.keys():
				if i in self.editor_instance.keys():
						pass
				else:
					data = i
					break
				i = i + 1
			else:
				data = i

		self.so[data] = scroll
		self.editor_instance[data] = self.editor
		label = self.create_tab_label(lbl, scroll, data)
		self.set_tab_label_packing(scroll, 0, 0, gtk.PACK_START)
		self.set_tab_label(scroll, label)
		label.show_all()
		self.show_all()
		
	def create_tab_label(self, title, scrl, num, tips = None):
		box = gtk.HBox()
		if title == "Untitled" and num not in self.file.keys():
			if len(self.unsave) == 0:
				val = 0
			else:
				i = 0
				for x in self.unsave.values():
					if i in self.unsave.values():
						pass
					else:
						val = i
						break
					i = i + 1
				else:
					val = i

			lab = title + " " + str(val + 1)
			self.unsave[num] = val
		else:
			lab = title
		label = gtk.Label(lab)
		btn_close = gtk.Button()
		icon = gtk.Image()
		icon.set_from_stock(gtk.STOCK_JUSTIFY_CENTER, gtk.ICON_SIZE_MENU)
		image = gtk.Image()
		image.set_from_stock(gtk.STOCK_CLOSE, gtk.ICON_SIZE_MENU)
		btn_close.set_image(image)
		btn_close.set_relief(gtk.RELIEF_NONE)
		btn_close.set_tooltip_text("Close file")

		if tips != None:
			box.set_tooltip_markup("<b>Path : </b>%s" % tips)

		box.pack_start(icon)
		box.pack_start(label, padding  = 5)
		box.pack_end(btn_close)
		btn_close.connect("clicked", self.close_tab, scrl)
		return box

	def close_tab(self, widget, child):
		scheme = child.get_children()[0].get_buffer().get_style_scheme()
		data = None
		val = 1
		i = 0
		for x in self.so:
			if child == self.so.values()[i]:
				data = self.so.keys()[i]
			i = i + 1
		
		buff = self.editor_instance[data].get_buffer()
		check = self.check_for_save(buff, data)
		hbox = self.get_tab_label(child)
		label_of_tab = hbox.get_children()
		text_of_tab = label_of_tab[1].get_text()
		
		if check == None:
			self.close_the_tab(child, data)
		elif check == -1:
			val = 0
			pass
		elif check:
			if self.save_current(text_of_tab, self.editor_instance[data], data):
				self.close_the_tab(child, data)			
			else:
				val = 0
				pass
		else:
			self.close_the_tab(child, data)
			
		if len(self.file) != 0:
			if data in self.file.keys():
				if val:
					j = 0
					for y in self.file.keys():
						if data == self.file.keys()[j]:
							del(self.file[data])
							break
						j= j + 1

		if len(self.editor_instance) == 0:
			self.new_tab("Untitled")
			self.editor_instance[0].get_buffer().set_style_scheme(scheme)
	
	def close_the_tab(self, boy, money):
		pagenum = self.page_num(boy)
		self.remove_page(pagenum)
		del(self.so[money])
		del(self.editor_instance[money])
		if money in self.unsave.keys():
			del(self.unsave[money])
	
	def check_for_save(self, buffer, num):
		val = None
		if buffer.get_modified():
			if  num in self.file.keys():
				file = os.path.basename(self.file[num])
			else:
				file = "Untitled " + str(self.unsave[num] + 1)
				
			message = "The document '%s' has been modified." % file+chr(13)+"Do you want to save the changes you have made ?"
			msg = gtk.MessageDialog(self.prnt, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_NONE, message)
			msg.set_title("Close document")
			msg.format_secondary_text("")
			msg.add_button(gtk.STOCK_SAVE, gtk.RESPONSE_YES)
			msg.add_button(gtk.STOCK_NO, gtk.RESPONSE_NO)
			msg.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
			
			respon = msg.run()
			
			if respon == gtk.RESPONSE_YES:
				val = 1
			elif respon == gtk.RESPONSE_NO:
				val = 0
			else:
				val = -1
			msg.destroy()
		return val
	
	def save_as_file(self, edit, index, text):
		def ask_for_replace(d_save):
			return gtk.FILE_CHOOSER_CONFIRMATION_CONFIRM
			
		ok = 0
		data = None
		d_save = gtk.FileChooserDialog("Save as..", self.prnt, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
		d_save.set_default_response(gtk.RESPONSE_OK)
		d_save.set_current_name(text)
		d_save.set_do_overwrite_confirmation(1)
		d_save.connect("confirm-overwrite", ask_for_replace)
		
		respon = d_save.run()
		
		if respon == gtk.RESPONSE_OK:
			file = d_save.get_filename()
			d_save.destroy()
			self.save_the_file(file, edit, index)
			ok = 1
		else:
			d_save.destroy()

		self.set_current_page(self.get_current_page())
		return ok

	def save_the_file(self, filename, data, key):
		try:
			out_file = open(filename, "w")
			if out_file:
				out_file.write(data._get_text())
				out_file.close()
		
			if using_gio:
				f = gio.File(filename)
				path = f.get_path()
				info = f.query_info("*")
	
				try:
					mime_type = info.get_content_type()
					language = None
				except:
					mime_type = "text/plain"
					language = None

			if using_gnomevfs:
				if os.path.isabs(filename):
					path = filename
				else:
					path = os.path.abspath(filename)

				try:
					mime_type = gnomevfs.get_mime_type(path)
					language = None
				except:
					mime_type = "text/plain"
					language = None

			if mime_type:
				language= ed.get_language_for_mime_type(mime_type)
			else:
				self.error_message("Error", "Could not get for mime type %s" % mime_type, self.prnt)

			self.md5[key] = self.md5checksum(data._get_text())
			self.file[key] = filename
			data.get_buffer().set_modified(0)
			data.get_buffer().set_language(language)
			if key in self.unsave.keys():
				del(self.unsave[key])
			self.set_label(os.path.basename(filename), data.get_parent(), key, filename)
			self.timer_id()
			string  = self.reset_status(key)
			if string != None:
				self.status.show_status("saving file \'%s\' ..." % string)
			return 1
			
		except:
			sec = "Check that you have write access to this file !"
			self.error_message("Error", "Could not save file '%s'" %filename, self.prnt, sec)
			return 1

	def save_current(self, text_of_tab, editor, key):
		if text_of_tab[:8] != "Untitled" or key in self.file.keys():
			if text_of_tab[2:][:8] != "Untitled" or key in self.file.keys():
				name_of_file = self.file[key]
				if self.save_the_file(name_of_file, editor, key):
					return 1
			else:
				if self.save_as_file(editor, key, text_of_tab[2:]):
					return 1
		else:
			if self.save_as_file(editor, key, text_of_tab):
				return 1
