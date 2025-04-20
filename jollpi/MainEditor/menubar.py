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
import gtk
import os
import re
import gobject

import help as help

try:
	import gio
	using_gio = 1
	using_gnomevfs = 0
except ImportError:
	import gnomevfs
	using_gio = 0
	using_gnomevfs = 1

(COL_BOOL, COL_STRING) = range(2)

find_ui ="""
<?xml version="1.0"?>
<interface>
  <object class="GtkWindow" id="find_window">
    <property name="title" translatable="yes">Find</property>
    <property name="resizable">False</property>
    <property name="modal">True</property>
    <property name="window_position">GTK_WIN_POS_CENTER</property>
    <property name="skip_taskbar_hint">True</property>
    <signal handler="on_find_window_delete_event" name="delete_event"/>
    <child>
      <object class="GtkVBox" id="vbox1">
        <property name="visible">True</property>
        <child>
          <object class="GtkFrame" id="frame1">
            <property name="visible">True</property>
            <property name="label_xalign">0</property>
            <child>
              <object class="GtkAlignment" id="alignment1">
                <property name="visible">True</property>
                <property name="left_padding">12</property>
                <child>
                  <object class="GtkVBox" id="vbox2">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkLabel" id="label3">
                        <property name="visible">True</property>
                        <property name="xalign">0</property>
                        <property name="label" translatable="yes">Text to find :</property>
                        <property name="wrap">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkEntry" id="txt_find">
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <signal handler="on_txt_find_changed" name="changed"/>
                      </object>
                      <packing>
                        <property name="fill">False</property>
                        <property name="padding">4</property>
                        <property name="position">1</property>
                      </packing>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child type="label">
              <object class="GtkLabel" id="label1">
                <property name="visible">True</property>
                <property name="label" translatable="yes">Find</property>
                <property name="use_markup">True</property>
              </object>
            </child>
          </object>
        </child>
        <child>
          <object class="GtkFrame" id="frame2">
            <property name="visible">True</property>
            <property name="label_xalign">0</property>
            <child>
              <object class="GtkAlignment" id="alignment2">
                <property name="visible">True</property>
                <property name="left_padding">12</property>
                <child>
                  <object class="GtkVBox" id="vbox3">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkCheckButton" id="chk_find_case_sensitive">
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="label" translatable="yes">Case sensitive</property>
                        <property name="draw_indicator">True</property>
                        <signal handler="on_chk_case_sensitive_toggled" name="toggled"/>
                      </object>
                      <packing>
                        <property name="fill">False</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkDrawingArea" id="drawingarea2">
                        <property name="visible">True</property>
                      </object>
                      <packing>
                        <property name="padding">15</property>
                        <property name="position">1</property>
                      </packing>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child type="label">
              <object class="GtkLabel" id="label2">
                <property name="visible">True</property>
                <property name="label" translatable="yes">Option</property>
                <property name="use_markup">True</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkHBox" id="hbox1">
            <property name="visible">True</property>
            <child>
              <object class="GtkDrawingArea" id="drawingarea1">
                <property name="visible">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="padding">85</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="btn_find">
                <property name="visible">True</property>
                <property name="sensitive">False</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="label" translatable="yes">gtk-find</property>
                <property name="use_stock">True</property>
                <signal handler="on_btn_find_clicked" name="clicked"/>
              </object>
              <packing>
                <property name="padding">5</property>
                <property name="position">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="btn_close">
                <property name="visible">True</property>
                <property name="receives_default">True</property>
                <property name="label" translatable="yes">gtk-close</property>
                <property name="use_stock">True</property>
                <signal handler="on_find_window_delete_event" name="clicked"/>
              </object>
              <packing>
                <property name="padding">4</property>
                <property name="position">2</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="padding">4</property>
            <property name="position">2</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
</interface>
"""

replace_ui = """
<?xml version="1.0"?>
<interface>
  <object class="GtkWindow" id="replace_window">
    <property name="title" translatable="yes">Replace</property>
    <property name="resizable">False</property>
    <property name="modal">True</property>
    <property name="window_position">GTK_WIN_POS_CENTER</property>
    <property name="skip_taskbar_hint">True</property>
    <signal handler="on_replace_window_delete_event" name="delete_event"/>
    <child>
      <object class="GtkVBox" id="vbox1">
        <property name="visible">True</property>
        <child>
          <object class="GtkFrame" id="frame1">
            <property name="visible">True</property>
            <property name="label_xalign">0</property>
            <child>
              <object class="GtkAlignment" id="alignment1">
                <property name="visible">True</property>
                <property name="left_padding">12</property>
                <child>
                  <object class="GtkVBox" id="vbox2">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkLabel" id="label3">
                        <property name="visible">True</property>
                        <property name="xalign">0</property>
                        <property name="label" translatable="yes">Text to find :</property>
                        <property name="wrap">True</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkEntry" id="txt_find_repl">
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <signal handler="on_txt_find_repl_changed" name="changed"/>
                      </object>
                      <packing>
                        <property name="fill">False</property>
                        <property name="padding">4</property>
                        <property name="position">1</property>
                      </packing>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child type="label">
              <object class="GtkLabel" id="label1">
                <property name="visible">True</property>
                <property name="label" translatable="yes">Find</property>
                <property name="use_markup">True</property>
              </object>
            </child>
          </object>
        </child>
        <child>
          <object class="GtkFrame" id="frame3">
            <property name="visible">True</property>
            <property name="label_xalign">0</property>
            <child>
              <object class="GtkAlignment" id="alignment3">
                <property name="visible">True</property>
                <property name="left_padding">12</property>
                <child>
                  <object class="GtkVBox" id="vbox5">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkLabel" id="label5">
                        <property name="visible">True</property>
                        <property name="xalign">0</property>
                        <property name="label" translatable="yes">Replace with :</property>
                      </object>
                    </child>
                    <child>
                      <object class="GtkEntry" id="txt_repl">
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                      </object>
                      <packing>
                        <property name="padding">4</property>
                        <property name="position">1</property>
                      </packing>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child type="label">
              <object class="GtkLabel" id="label4">
                <property name="visible">True</property>
                <property name="label" translatable="yes">Replace</property>
                <property name="use_markup">True</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="position">1</property>
          </packing>
        </child>
        <child>
          <object class="GtkFrame" id="frame2">
            <property name="visible">True</property>
            <property name="label_xalign">0</property>
            <child>
              <object class="GtkAlignment" id="alignment2">
                <property name="visible">True</property>
                <property name="left_padding">12</property>
                <child>
                  <object class="GtkVBox" id="vbox3">
                    <property name="visible">True</property>
                    <child>
                      <object class="GtkCheckButton" id="chk_repl_case_sensitive">
                        <property name="visible">True</property>
                        <property name="can_focus">True</property>
                        <property name="label" translatable="yes">Case sensitive</property>
                        <property name="draw_indicator">True</property>
                        <signal handler="on_chk_repl_case_sensitive_toggled" name="toggled"/>
                      </object>
                      <packing>
                        <property name="fill">False</property>
                      </packing>
                    </child>
                    <child>
                      <object class="GtkDrawingArea" id="drawingarea2">
                        <property name="visible">True</property>
                      </object>
                      <packing>
                        <property name="padding">15</property>
                        <property name="position">1</property>
                      </packing>
                    </child>
                  </object>
                </child>
              </object>
            </child>
            <child type="label">
              <object class="GtkLabel" id="label2">
                <property name="visible">True</property>
                <property name="label" translatable="yes">Option</property>
                <property name="use_markup">True</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="position">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkHBox" id="hbox1">
            <property name="visible">True</property>
            <child>
              <object class="GtkDrawingArea" id="drawingarea1">
                <property name="visible">True</property>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">False</property>
                <property name="padding">65</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="btn_replace">
                <property name="visible">True</property>
                <property name="sensitive">False</property>
                <property name="can_focus">True</property>
                <property name="receives_default">True</property>
                <property name="label" translatable="yes">gtk-find-and-replace</property>
                <property name="use_stock">True</property>
                <signal handler="on_btn_replace_clicked" name="clicked"/>
              </object>
              <packing>
                <property name="padding">5</property>
                <property name="position">1</property>
              </packing>
            </child>
            <child>
              <object class="GtkButton" id="btn_repl_close">
                <property name="visible">True</property>
                <property name="receives_default">True</property>
                <property name="label" translatable="yes">gtk-close</property>
                <property name="use_stock">True</property>
                <signal handler="on_replace_window_delete_event" name="clicked"/>
              </object>
              <packing>
                <property name="padding">4</property>
                <property name="position">2</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="padding">4</property>
            <property name="position">3</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
</interface>
"""

ui_info = """
<ui>
	<menubar name = "MenuBar">
		<menu action = "file">
			<menuitem action = "new"/>
			<menuitem action = "open"/>
			<separator/>
			<menuitem action = "save"/>
			<menuitem action = "save_as"/>
			<separator/>
			<menuitem action = "pagesetup"/>
			<separator/>
			<menuitem action = "print"/>
			<separator/>
			<menuitem action = "close"/>
			<menuitem action = "quit"/>
		</menu>
		<menu action = "edit">
			<menuitem action = "undo"/>
			<menuitem action = "redo"/>
			<separator/>
			<menuitem action = "cut"/>
			<menuitem action = "copy"/>
			<menuitem action = "paste"/>
			<menuitem action = "select_all"/>
			<separator/>
			<menuitem action = "delete"/>
		</menu>
		<menu action = "search">
			<menuitem action = "find"/>
			<menuitem action = "find_next"/>
			<menuitem action = "find_prev"/>
			<menuitem action = "replace"/>
			<menuitem action = "goto_line"/>
		</menu>
		<menu action = "view">
			<menu action = "wrap">
				<menuitem action = "none"/>
				<menuitem action = "char"/>
				<menuitem action = "word"/>
			</menu>
			<menu action = "style">
				<menuitem action = "kate"/>
				<menuitem action = "classic"/>
				<menuitem action = "tango"/>
				<menuitem action = "oblivion"/>
				<menuitem action = "jollpi"/>
			</menu>
			<separator/>
			<menuitem action = "indent"/>
			<menuitem action = "number"/>
			<menuitem action = "mark"/>
			<menuitem action = "margin"/>
			<separator/>
			<menuitem action = "font"/>
		</menu>
		<menu action = "help">
			<menuitem action = "docs"/>
			<menuitem action = "about"/>
		</menu>
	</menubar>
</ui>
"""

class MenuBar:
	def __init__(self, window, editor, stbar, stbar1, stbar2, tabs):
		global helps
		global ed
		global tab
		global status
		global status1
		global status2
		helps = help.Help()
		ed = editor
		status = stbar
		status1 = stbar1
		status2 = stbar2
		tab = tabs
		tab.connect("switch-page", self.switch_page)
		
		self.key = None
		self.data = None
		self.filename = tab.file
		self.id = 0
		self.ids = 0
		self.count = 0
		self.cs_find = 0
		self.cs_repl = 0
		self.find_string = ""
		self.current_line = -1
		self.setting = None
		self.p_setup = None
		
		find_builder = gtk.Builder()
		find_builder.add_from_string(find_ui,len(find_ui))
		find_builder.connect_signals(self)
		self.find_window = find_builder.get_object("find_window")
		self.btn_find = find_builder.get_object("btn_find")
		self.txt_find = find_builder.get_object("txt_find")
		self.txt_find.connect("key-press-event", self.cancel_show_window)
		self.txt_find.connect("key-release-event", self.txt_find_release)
		self.chk_find_case_sensitive = find_builder.get_object("chk_find_case_sensitive")
		self.chk_find_case_sensitive.connect("key-press-event", self.cancel_show_window)
		
		replace_builder = gtk.Builder()
		replace_builder.add_from_string(replace_ui, len(replace_ui))
		replace_builder.connect_signals(self)
		self.replace_window = replace_builder.get_object("replace_window")
		self.btn_replace = replace_builder.get_object("btn_replace")
		self.txt_find_repl = replace_builder.get_object("txt_find_repl")
		self.txt_repl = replace_builder.get_object("txt_repl")
		self.txt_find_repl.connect("key-press-event", self.cancel_show_window)
		self.txt_repl.connect("key-press-event", self.cancel_show_window)
		
		self.txt_find_repl.connect("key-release-event", self.txt_repl_release)
		self.txt_repl.connect("key-release-event", self.txt_repl_release)
		self.chk_repl_case_sensitive = replace_builder.get_object("chk_repl_case_sensitive")
		self.chk_repl_case_sensitive.connect("key-press-event", self.cancel_show_window)
		
		scheme = gtksourceview.style_scheme_manager_get_default()
		self.style = scheme.get_scheme("kate")
	
	def create_menu(self, window):
		entries = [
			("file", gtk.STOCK_EXECUTE, "_File"),
			("edit", gtk.STOCK_EDIT, "_Edit"),
			("search", gtk.STOCK_SELECT_FONT, "_Search"),
			("view", gtk.STOCK_SELECT_COLOR, "_View"),
			("help", gtk.STOCK_HOME, "_Help"),
			("new", gtk.STOCK_NEW, "_New", "<control>N", None, self.new),
			("open", gtk.STOCK_OPEN, "_Open...", "<control>O", None, self.open),
			("save", gtk.STOCK_SAVE, "_Save", "<control>S", None, self.save_current_file),
			("save_as", gtk.STOCK_SAVE_AS, "Save _As...", "<shift><control>S", None, self.save_as),
			("pagesetup", gtk.STOCK_PREFERENCES, "Page Set_up", None, None, self.page_setup),
			("print", gtk.STOCK_PRINT, "Print...", "<control>P", None, self.print_page),
			("close", gtk.STOCK_CLOSE, "_Close", "<control>W", None, self.close),
			("quit", gtk.STOCK_QUIT, "_Quit", "<control>Q", None, self.quit),
			("undo", gtk.STOCK_UNDO, "_Undo", "<control>Z", None, self.undo),
			("redo", gtk.STOCK_REDO, "_Redo", "<shift><control>Z", None, self.redo),
			("cut", gtk.STOCK_CUT, "Cu_t", "<control>X", None, self.cut),
			("copy", gtk.STOCK_COPY, "_Copy", "<control>C", None, self.copy),
			("paste", gtk.STOCK_PASTE, "_Paste", "<control>V", None, self.paste),
			("select_all", gtk.STOCK_SELECT_ALL, "Select _All", "<control>A", None, self.select_all),
			("delete", gtk.STOCK_DELETE, "_Delete", None, None, self.delete),
			("find", gtk.STOCK_FIND, "_Find...", "<control>F", None, self.find),
			("find_next", gtk.STOCK_GO_FORWARD, "Find _Next", "F3", None, self.find_next),
			("find_prev", gtk.STOCK_GO_BACK, "Find _Pre_vious", "<shift>F3", None, self.find_previous),
			("replace", gtk.STOCK_FIND_AND_REPLACE, "_Replace...", "<control>R", None, self.replace),
			("goto_line", gtk.STOCK_JUMP_TO, "Go to _Line...", "<control>G", None, self.show_goto_line),
			("font", gtk.STOCK_INDEX, "Select _Font...", "F6", None, self.select_font_clicked),
			("wrap", None, "W_rap"),
			("style", None, "_Highlighting Style"),
			("docs", gtk.STOCK_HELP, "_Contents", "F1", None, self.show_docs),
			("about", gtk.STOCK_ABOUT, "A_bout", None, None, self.show_about)
			]
			
		toggle = [
			("indent", None, "_Enable Auto Indent", "F8", None, self.enable_auto_indent, 0),
			("number", None, "Show _Line Numbers", "F11", None, self.show_line_numbers),
			("mark", None, "Show Line _Marks", "F9", None, self.show_line_marks),
			("margin", None, "Show _Right Margin", "F7", None, self.show_right_margin)
			]
			
		radio1 = [
			("none", None, "_None", None, None, 1),
			("char", None, "_Character", None, None, 2),
			("word", None, "_Word", None, None, 3)
			]
			
		radio2 = [
			("kate", None, "_Kate", None, None, 1),
			("classic", None, "_Classic", None, None, 2),
			("tango", None, "_Tango", None, None, 3),
			("oblivion", None, "_Oblivion", None, None, 4),
			("jollpi", None, "_Jollpi", None, None, 5)
			]

		actions = gtk.ActionGroup("actions")
		actions.add_actions(entries)
		actions.add_toggle_actions(toggle)
		actions.add_radio_actions(radio1, -1, self.set_wrap)
		actions.add_radio_actions(radio2, -1, self.set_scheme)
		
		ui = gtk.UIManager()
		#window.set_data("ui-manager", ui)
		ui.insert_action_group(actions, 0)
		window.add_accel_group(ui.get_accel_group())
		ui.add_ui_from_string(ui_info)
		menubar = ui.get_widget("/MenuBar")

		get_widget = [
			{"/MenuBar/file/new" : "Create a new file"},
			{"/MenuBar/file/open" : "Open a file"},
			{"/MenuBar/file/save" : "Save the current file"},
			{"/MenuBar/file/save_as" : "Save the current file with a different name"},
			{"/MenuBar/file/print" : "Print the current page"},
			{"/MenuBar/file/pagesetup" : "Setup the page settings"},
			{"/MenuBar/file/close" : "Close the active file"},
			{"/MenuBar/file/quit" : "Quit the application"},
			{"/MenuBar/edit/undo" : "Undo the las editing command"},
			{"/MenuBar/edit/redo" : "Redo the last undo step"},
			{"/MenuBar/edit/cut" : "Cut selected text"},
			{"/MenuBar/edit/copy" : "Copy selected text"},
			{"/MenuBar/edit/paste" : "Paste the clipboard"},
			{"/MenuBar/edit/select_all" : "Select all text"},
			{"/MenuBar/edit/delete" : "Delete the selected text"},
			{"/MenuBar/search/find" : "Search for text"},
			{"/MenuBar/search/find_next" : "Search forward for the same text"},
			{"/MenuBar/search/find_prev" : "Search backward for the same text"},
			{"/MenuBar/search/replace" : "Search for and replace text"},
			{"/MenuBar/search/goto_line" : "Go to spesific line"},
			{"/MenuBar/view/wrap/none" : "Don't wrap lines"},
			{"/MenuBar/view/wrap/char" : "Wrap text, breaking lines in between characters"},
			{"/MenuBar/view/wrap/word" : "Wrap text, breaking lines in between words"},
			{"/MenuBar/view/style/kate" : "Use Kate style"},
			{"/MenuBar/view/style/classic" : "Use Classic style"},
			{"/MenuBar/view/style/tango" : "Use Tango style"},
			{"/MenuBar/view/style/oblivion" : "Use Oblivion style"},
			{"/MenuBar/view/style/jollpi" : "Use Jollpi style"},
			{"/MenuBar/view/indent" : "Enable or disable auto indent"},
			{"/MenuBar/view/number" : "Show or hide line numbers"},
			{"/MenuBar/view/mark" : "Show or hide line marks"},
			{"/MenuBar/view/margin" : "Show or hide right margin"},
			{"/MenuBar/view/font" : "Change familiy, style, or size for current font"},
			{"/MenuBar/help/docs" : "Show the help browser"},
			{"/MenuBar/help/about" : "About this application"}
			]

		self.x_undo = ui.get_widget(get_widget[8].keys()[0])
		self.x_redo = ui.get_widget(get_widget[9].keys()[0])
		self.x_cut = ui.get_widget(get_widget[10].keys()[0])
		self.x_copy = ui.get_widget(get_widget[11].keys()[0])
		self.x_delete = ui.get_widget(get_widget[14].keys()[0])
		self.x_undo.set_sensitive(0)
		self.x_redo.set_sensitive(0)
		self.x_cut.set_sensitive(0)
		self.x_copy.set_sensitive(0)
		self.x_delete.set_sensitive(0)
		
		self.indent = ui.get_widget(get_widget[28].keys()[0])
		self.number = ui.get_widget(get_widget[29].keys()[0])
		self.mark = ui.get_widget(get_widget[30].keys()[0])
		self.margin = ui.get_widget(get_widget[31].keys()[0])
		self.indent.set_active(1)
		self.number.set_active(1)
		self.mark.set_active(1)
		
		for x in get_widget:
			tes = ui.get_widget(x.keys()[0])
			tes.connect("select", self.select, x.values()[0])
			tes.connect("deselect", self.deselect, x.values()[0])

		self.parent = window
		self.eid = self.parent.connect("expose-event", self.changed_on_the_disk)
		self.parent.connect("focus-out-event", self.focus_out)
		return menubar
	
	def warning_message(self, title, message, parent):
		msg =  gtk.MessageDialog(parent, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, message)
		msg.set_title(title)
		msg.format_secondary_text("")
		msg.run()
		msg.destroy()
	
	def changed_on_the_disk(self, widget, event):
		child = tab.get_nth_page(tab.get_current_page())
		i = 0
		for x in tab.so:
			if tab.so.values()[i] == child:
				key = tab.so.keys()[i]
			i = i + 1
			
		if key in self.filename.keys():
			try:
				old_f = self.filename[key]
				file = open(old_f, "rb")
				hashing = tab.md5checksum(file.read())
				file.close()
				
				if hashing != tab.md5[key]:
					if not self.id and not self.ids:
						self.id = 1
						message = "The file '%s' was modified by another program." % self.filename[key]
						msg = gtk.MessageDialog(self.parent, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK_CANCEL, message)
						msg.format_secondary_text("Do you want to reload the file ?")
						msg.set_title("File Changed on Disk")
				
						run = msg.run()
							
						if run == gtk.RESPONSE_OK:
							self.count = 0
							self.open_file(old_f, self.count)
						else:
							self.ids = 1
							
						self.id = 0
						msg.destroy()
			except:
				if not self.id and not self.ids:
					self.id = 1
					message = "The file %s was deleted by another program" % self.filename[key]
					msg = gtk.MessageDialog(self.parent, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_NONE, message)
					msg.set_title("File was Deleted on Disk")
					msg.add_button(gtk.STOCK_SAVE_AS, gtk.RESPONSE_YES)
					msg.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
					msg.format_secondary_text("What do you want to do ?")
					
					run = msg.run()
					
					if run == gtk.RESPONSE_YES:
						msg.destroy()
						num = key
						del(self.filename[key])
						if tab.save_as_file(tab.editor_instance[key], key, os.path.basename(old_f)):
							pass
						else:
							self.filename[num] = old_f
					else:
						self.ids = 1
						msg.destroy()

					self.id = 0
	
	def focus_out(self, widget, event):
		if self.ids:
			self.ids = 0

	def select(self, widget, msg):
		status.show_status(msg)
		
	def deselect(self, widget, msg):
		tab.clear()
		
	def on_text_buffer_modified_changed(self, buff):
		if buff.get_modified():
			if not self.parent.get_title()[0] == "~":
				self.parent.set_title("~ " + self.parent.get_title())

			self.x_undo.set_sensitive(1)
			self.tu.set_sensitive(1)

		regex = re.compile("(\s\-\sJOLLPI)$")
		label = regex.split(self.parent.get_title())
		i = 0
		for x in self.filename:
			lbl = os.path.basename(self.filename.values()[i])
			if label[0] == lbl or label[0][2:] == lbl:
				tab.set_label(label[0], self.data.get_parent(), self.key, self.filename.values()[i])
				break
			i = i + 1
		else:
			tab.set_label(label[0], self.data.get_parent(), self.key)
	
	def on_text_buffer_mark_set(self, buff, loc, mark):
		status1.show_line_col(buff)
		
		if buff.get_selection_bounds() != ():
			self.x_cut.set_sensitive(1)
			self.x_copy.set_sensitive(1)
			self.tct.set_sensitive(1)
			self.tcp.set_sensitive(1)
			self.x_delete.set_sensitive(1)
			self.txt_find.set_text(self.buff.get_slice(self.buff.get_selection_bounds()[0], self.buff.get_selection_bounds()[1]))
			self.txt_find_repl.set_text(self.buff.get_slice(self.buff.get_selection_bounds()[0], self.buff.get_selection_bounds()[1]))
		else:
			self.x_cut.set_sensitive(0)
			self.x_copy.set_sensitive(0)
			self.tct.set_sensitive(0)
			self.tcp.set_sensitive(0)
			self.x_delete.set_sensitive(0)

	def line_col(self, buff):
		status1.show_line_col(buff)
		
	def overwrite(self, widget, key):
		ci = status2.get_context_id("Status Bar2")
		if key.keyval == 65379:
			if self.data.get_overwrite():
				status2.push(ci, "INS")
			else:
				status2.push(ci, "OVR")
	
	def switch_page(self, widget, page, pagenum):
		if self.ids:
			self.ids = 0
		style = None
		text_of_tab = None
		child = tab.get_nth_page(pagenum)
		hbox = tab.get_tab_label(child)
		self.key, self.data = tab.get_values(child)
		if hbox == None:
			pass
		else:
			label_of_tab = hbox.get_children()
			text_of_tab = label_of_tab[1].get_text()
			
		self.parent.set_title("%s - JOLLPI" % text_of_tab)

		try:
			self.data.connect("key-press-event", self.overwrite)
			status2.change_overwrite(self.data)
			
			self.buff = self.data.get_buffer()
			self.buff.connect("modified-changed", self.on_text_buffer_modified_changed)
			self.buff.connect("mark-set", self.on_text_buffer_mark_set)
			self.buff.connect("changed", self.line_col)
			status1.show_line_col(self.buff)
			self.buff.set_style_scheme(self.style)
			
			if self.buff.can_undo():
				self.x_undo.set_sensitive(1)
				self.tu.set_sensitive(1)
			else:
				self.x_undo.set_sensitive(0)
				self.tu.set_sensitive(0)
				
			if self.buff.can_redo():
				self.x_redo.set_sensitive(1)
				self.tr.set_sensitive(1)
			else:
				self.x_redo.set_sensitive(0)
				self.tr.set_sensitive(0)
			
			if self.number.get_active():
				self.data._set_show_line_numbers(1)
			else:
				self.data._set_show_line_numbers(0)
			if self.indent.get_active():
				self.data._set_auto_indent(1)
			else:
				self.data._set_auto_indent(0)
			if self.mark.get_active():
				self.data._set_show_line_marks(1)
			else:
				self.data._set_show_line_marks(0)
			if self.margin.get_active():
				self.data._set_show_right_margin(1)
			else:
				self.data._set_show_right_margin(0)
				
			self.data.set_font(self.win.get_font_name())
		except:
			pass

	def new(self, widget):
		tab.new_tab("Untitled")
		tab.set_current_page(tab.get_n_pages() - 1)

	def open(self, widget):
		filename = None
		list = []
		d_open = gtk.FileChooserDialog("Open..", self.parent, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
		d_open.set_select_multiple(1)
		d_open.set_default_response(gtk.RESPONSE_OK)

		respon = d_open.run()
						
		if respon == gtk.RESPONSE_OK:
			list = d_open.get_filenames()
			
		d_open.destroy()
		
		x = 0
		for i in list:
			filename = list[x]
			if filename in self.filename.values():
				pass
			else:
				self.count = 1
				self.open_file(filename, self.count)

			x = x + 1
		
	def open_file(self, filename, number):
		if using_gio:
			try:
				in_file = open(filename, "rb")
			except:
				sec = "check if it exist or you have read access to this file !"
				tab.error_message("Error", "Could not open file : '%s'" % filename, self.parent, sec)
			
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
				in_file = open(path, "rb")
			except:
				sec = "check if it exist or you have read access to this file !"
				tab.error_message("Error", "Could not open file '%s'" % filename, self.parent, sec)
				
			try:
				mime_type = gnomevfs.get_mime_type(path)
				language = None
			except:
				mime_type = "text/plain"
				language = None
			
		if mime_type:
			language = ed.get_language_for_mime_type(mime_type)
			if (not language) and (mime_type[0:4] != "text"):
				tab.info_message("Binary file opened", "The file '%s' is binary, content will not show" % filename, self.parent)
			else:
				try:
					if in_file:
						text = in_file.read()
						if number:
							tab.new_tab(os.path.basename(filename))
							tab.set_current_page(tab.get_n_pages() - 1)
							tab.md5[self.key] = tab.md5checksum(text)
							self.filename[self.key] = filename
							self.buff.begin_not_undoable_action()
							self.data._set_text(text)
							string = tab.reset_status(self.key)
							if string != None:
								status.show_status("loading file \'%s\' ..." % string)
							in_file.close()
							tab.timer_id()
							self.data.set_language(language)
							self.buff.set_modified(0)
							self.buff.end_not_undoable_action()
						else:
							tab.md5[self.key] = tab.md5checksum(text)
							in_file.close()
							self.buff.begin_not_undoable_action()
							self.data._set_text(text)
							self.buff.set_modified(0)
							self.buff.end_not_undoable_action()
							tab.set_label(os.path.basename(filename), tab.so[self.key], self.key, filename)
							self.parent.set_title("%s - JOLLPI" % os.path.basename(filename))

					self.x_undo.set_sensitive(0)
					self.x_redo.set_sensitive(0)
					self.tu.set_sensitive(0)
					self.tr.set_sensitive(0)
				except:
					return 0
		else:
			tab.error_message("Error", "Could not get for mime type %s" % mime_type, self.parent)
			pass

	def save_as(self, widget):
		text_of_tab = tab.get_label()
		if text_of_tab[2:][:8] != "Untitled":
			tab.save_as_file(self.data, self.key, text_of_tab)
		else:
			tab.save_as_file(self.data, self.key, text_of_tab[2:])

	def save_current_file(self, widget):
		text_of_tab = tab.get_label()
		tab.save_current(text_of_tab, self.data, self.key)
	
	def page_setup(self, widget):
		if self.setting is None:
			self.setting = gtk.PrintSettings()
		self.p_setup = gtk.print_run_page_setup_dialog(self.parent, self.p_setup, self.setting)
	
	def print_page(self, widget):
		compositor = gtksourceview.print_compositor_new_from_view(self.data)
		compositor.set_wrap_mode(gtk.WRAP_CHAR)
		compositor.set_highlight_syntax(1)
		compositor.set_print_line_numbers(1)
		compositor.set_header_format(0, "Printed on %A, %d-%m-%Y", None, "by JOLLPI")
		try:
			name = self.filename[self.key]
		except:
			name = "Untitled"
		compositor.set_footer_format(1, "%T", name, "Page %N/%Q")
		compositor.set_print_header(1)
		compositor.set_print_footer(1)
		
		print_op = gtk.PrintOperation()
		print_op.set_show_progress(1)
		
		if self.setting is not None:
			print_op.set_print_settings(self.setting)
			
		if self.p_setup is not None:
			print_op.set_default_page_setup(self.p_setup)

		print_op.connect("begin-print", self.begin_print, compositor)
		print_op.connect("draw-page", self.draw_page, compositor)
		res = print_op.run(gtk.PRINT_OPERATION_ACTION_PRINT_DIALOG, self.parent)
		
		if res == gtk.PRINT_OPERATION_RESULT_ERROR:
			tab.error_message("Error", "Error printing file : '%s'" % name, self.parent)
		elif res == gtk.PRINT_OPERATION_RESULT_APPLY:
			tab.info_message("Information", "File printed: '%s'" % name, self.parent)
		
	def begin_print(self, operation, context, composit):
		while not composit.paginate(context):
			pass
		n_pages = composit.get_n_pages()
		operation.set_n_pages(n_pages)
		
	def draw_page(self, operation, context, page_nr, composit):
		composit.draw_page(context, page_nr)
		
	def preview(self, operation, preview , context, parent):
		operation.run(gtk.PRINT_OPERATION_ACTION_PREVIEW, None)
	
	def close(self, widget):
		tab.close_tab(self, tab.so[self.key])
	
	def quit(self, widget):
		data = []
		self.dat = []
		i = 0
		for x in tab.editor_instance:
			if tab.editor_instance.values()[i].get_buffer().get_modified():
				hbox = tab.get_tab_label(tab.so.values()[i])
				label_of_tab = hbox.get_children()
				text_of_tab = label_of_tab[1].get_text()
				data.append(1)
				data.append(text_of_tab)
				data.append(tab.editor_instance.values()[i])
				data.append(tab.editor_instance.keys()[i])
				self.dat.append(data)
				data = []
			i = i + 1
			
		if len(self.dat) == 0:
			gtk.main_quit()
		else:
			msg = "The following document have been modified. Save changes before closing ?"
			dialog = gtk.MessageDialog(self.parent, 0, gtk.MESSAGE_WARNING, gtk.BUTTONS_NONE, msg)
			dialog.set_title("Save documents")
			dialog.format_secondary_text("Select the documents you want to save") 
			dialog.add_button(gtk.STOCK_SAVE, gtk.RESPONSE_YES)
			dialog.add_button(gtk.STOCK_NO, gtk.RESPONSE_NO)
			dialog.add_button(gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL)
			box = gtk.VBox()
			sw = gtk.ScrolledWindow()
			sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
			sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_AUTOMATIC)
			box.pack_start(sw)
	
			model = gtk.ListStore(
				gobject.TYPE_BOOLEAN,
				gobject.TYPE_STRING,
			)

			for item in self.dat:
				iter = model.append()
				model.set(iter,
					COL_BOOL, item[COL_BOOL],
					COL_STRING, item[COL_STRING][2:])
					
			treeview = gtk.TreeView(model)
			treeview.set_size_request(0, 150)
			treeview.set_rules_hint(True)
			sw.add(treeview)
			renderer = gtk.CellRendererToggle()
			renderer.set_data("column", COL_BOOL)
			renderer.connect('toggled', self.fixed_toggled, model)
			column = gtk.TreeViewColumn('Check', renderer, active=COL_BOOL)
			column.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
			column.set_fixed_width(80)
			treeview.append_column(column)
			renderer = gtk.CellRendererText()
			renderer.set_data("column", COL_STRING)
			column = gtk.TreeViewColumn('Filename', renderer, text=COL_STRING)
			treeview.append_column(column)
			dialog.vbox.pack_start(box)
			dialog.show_all()
			respon = dialog.run()
			if respon == gtk.RESPONSE_YES:
				dialog.destroy()
				k = 0
				dict = tab.editor_instance.keys()
				for y in dict:
					edit = dict[k]
					j = 0
					for x in self.dat:
						if self.dat[j][3] == edit:
							if self.dat[j][0]:
								if tab.save_current(self.dat[j][1], self.dat[j][2], self.dat[j][3]):
									tab.close_tab(self, tab.so[self.dat[j][3]])
							else:
								tab.close_the_tab(tab.so[self.dat[j][3]], self.dat[j][3])
						j = j + 1
					k = k + 1
				else:
					l = 0
					for z in tab.editor_instance:
						if tab.editor_instance.values()[l].get_buffer().get_modified():
							break
						l = l + 1
					else:
						gtk.main_quit()
			elif respon == gtk.RESPONSE_NO:
				gtk.main_quit()
			elif respon == gtk.RESPONSE_CANCEL:
				pass
				dialog.destroy()
	
	def fixed_toggled(self, cell, path, model):
		iter = model.get_iter((int(path),))
		path = model.get_path(iter)[0]
		column = cell.get_data("column")
		if column == COL_BOOL:
			bool = model.get_value(iter, COL_BOOL)
			bool = not bool
			self.dat[path][COL_BOOL] = bool
			model.set(iter, COL_BOOL, bool)

	def undo(self, widget):
		if self.buff.can_undo():
			self.data._undo()
			self.x_redo.set_sensitive(1)
			self.tr.set_sensitive(1)

		if not self.buff.can_undo():
			self.x_undo.set_sensitive(0)
			self.tu.set_sensitive(0)
		
	def redo(self, widget):
		if self.buff.can_redo():
			self.data._redo()

		if not self.buff.can_redo():
			self.x_redo.set_sensitive(0)
			self.tr.set_sensitive(0)

	def cut(self, widget):
		self.data._cut()
	
	def copy(self, widget):
		self.data._copy()
			
	def paste(self, widget):
		self.data._paste()
		
	def select_all(self, widget):
		self.data._select_all()
		
	def delete(self, widget):
		self.data._delete()
		
	def cancel_show_window(self, widget, key):
		if key.keyval == 65307:
			self.find_window.hide_all()
			self.replace_window.hide_all()
	
	def find(self, widget):
		self.find_window.set_transient_for(self.parent)
		if self.find_window.get_property("visible"):
			self.find_window.present()
			return
			
		self.find_window.show_all()
		
	def on_find_window_delete_event(self, widget, key = None):
		self.find_window.hide_all()
	
	def do_find(self, iter, string, mode, model):
		flags = 0
		
		if model:
			if not self.cs_find:
				flags = gtksourceview.SEARCH_CASE_INSENSITIVE
		else:
			if not self.cs_repl:
				flags = gtksourceview.SEARCH_CASE_INSENSITIVE
		
		if mode:
			result = gtksourceview.iter_forward_search(iter, string, flags)
		else:
			result = gtksourceview.iter_backward_search(iter, string, flags)
			
		return result
		
	def on_txt_find_changed(self, widget):
		if self.txt_find.get_text() != "":
			self.btn_find.set_sensitive(1)
		else:
			self.btn_find.set_sensitive(0)
		
	def on_chk_case_sensitive_toggled(self, data = None):
		self.cs_find = not self.cs_find
	
	def on_btn_find_clicked(self, widget):
		mark = 1
		self.find_string = self.txt_find.get_text()
		
		try:
			find_iter = self.buff.get_iter_at_mark(self.buff.get_selection_bound())
			result = self.do_find(find_iter, self.find_string, mark, 1)
			self.buff.select_range(result[0], result[1])
			ed._scroll_to_mark(mark)
			self.find_window.hide_all()
		except:
			self.find_window.hide_all()
			
			try:
				find_iter = self.buff.get_start_iter()
				result = self.do_find(find_iter, self.find_string, mark, 1)
				self.buff.select_range(result[0], result[1])
				ed._scroll_to_mark(mark)
			except:
				self.warning_message("Find", "Search string '%s' not found !" % self.find_string, self.parent)
			
	def txt_find_release(self, widget, key):
		if key.keyval == 65293:
			self.on_btn_find_clicked(self)
	
	def find_next(self, widget):
		if self.find_string == "":
			self.find(self)
		else:
			self.on_btn_find_clicked(self)
		
	def find_previous(self, widget):
		mark = 0
		if self.find_string == "":
			self.find(self)

		try:
			find_iter = self.buff.get_iter_at_mark(self.buff.get_insert())
			result = self.do_find(find_iter, self.find_string, mark, 1)
			self.buff.select_range(result[0], result[1])
			ed._scroll_to_mark(mark)
			
		except:
			try:
				find_iter = self.buff.get_end_iter()
				result = self.do_find(find_iter, self.find_string, mark, 1)
				self.buff.select_range(result[1], result[0])
				ed._scroll_to_mark(mark)
			except:
				self.warning_message("Find", "Search string '%s' not found !" % self.find_string, self.parent)
	
	def replace(self, widget):
		self.replace_window.set_transient_for(self.parent)
		if self.replace_window.get_property("visible"):
			self.replace_window.present()
			return
		
		self.replace_window.show_all()
	
	def on_btn_replace_clicked(self, widget):
		self.search_string = self.txt_find_repl.get_text()
		self.repl_string = self.txt_repl.get_text()
		self.replace_window.hide_all()
		self.do_replace(self.buff, self.search_string, self.repl_string)
		
	def txt_repl_release(self, widget, key):
		if key.keyval == 65293:
			self.on_btn_replace_clicked(self)
		
	def do_replace(self, buff, find, replace):
		repl_start = buff.create_mark(None, buff.get_start_iter())
		repl_end = buff.create_mark(None, buff.get_end_iter())
		result = self.find_all_in_range(buff, find, repl_start, repl_end)
		
		result_marks = []
		for iteration in result:
			this_mark_match = []
			for iter in iteration:
				this_mark = buff.create_mark(None, iter)
				this_mark_match.append(this_mark)
				
			result_marks.append(this_mark_match)
			
		for mark in result_marks:
			begin = buff.get_iter_at_mark(mark[0])
			end = buff.get_iter_at_mark(mark[1])
			buff.delete(begin, end)
			buff.insert(begin, replace)
			
		if len(result) < 1:
			self.warning_message("Replace", "Search string '%s' not found !" % self.search_string, self.parent)
		else:
			tab.info_message("Replace", "%s Replacement made" % len(result), self.parent)
		
	def find_all_in_range(self, buf, string, start_mark, end_mark):
		start_iter = buf.get_iter_at_mark(start_mark)
		end_iter = buf.get_iter_at_mark(end_mark)
		search_results = []
		
		next = self.do_find(start_iter, string, 1, 0)
		while next:
			search_results.append(next)
			next = self.do_find(next[1], string, 1, 0)
			
		return search_results
				
	def on_replace_window_delete_event(self, widget):
		self.replace_window.hide_all()
		#return 0
		
	def on_txt_find_repl_changed(self, widget):
		if self.txt_find_repl.get_text() != "":
			self.btn_replace.set_sensitive(1)
		else:
			self.btn_replace.set_sensitive(0)
			
	def on_chk_repl_case_sensitive_toggled(self, data = None):
		self.cs_repl = not self.cs_repl
		
	def goto_line_window(self, up, val):
		self.w = gtk.Window()
		self.w.set_title("Go to Line")
		self.w.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.w.set_transient_for(self.parent)
		self.w.set_modal(1)
		self.w.set_resizable(0)
		box = gtk.VBox()
		lbl = gtk.Label("Go to line :")
		adj = gtk.Adjustment(lower = 1, upper = up, step_incr = 1, value = val)
		self.spin = gtk.SpinButton(adj)
		self.spin.connect("key-press-event", self.spin_press)
		self.spin.connect("key-release-event", self.spin_release)
		buttonbox = gtk.HButtonBox()
		buttonbox.set_border_width(10)
		buttonbox.set_layout(gtk.BUTTONBOX_START)
		buttonbox.set_spacing(10)
		btn_ok = gtk.Button(stock = gtk.STOCK_OK)
		btn_cancel =gtk.Button(stock = gtk.STOCK_CANCEL)
		btn_ok.connect("clicked", self.switch_line)
		btn_cancel.connect("clicked", self.hide_goto_line)
		buttonbox.add(btn_ok)
		buttonbox.add(btn_cancel)
		box.pack_start(lbl, padding = 5)
		box.pack_start(self.spin)
		box.pack_start(buttonbox)
		self.w.add(box)
	
	def show_goto_line(self, widget):
		iter = self.buff.get_iter_at_mark(self.buff.get_insert())
		lines = self.buff.get_line_count()
		line_pos = iter.get_line() + 1
		
		self.goto_line_window(lines, line_pos)
		self.w.show_all()
	
	def switch_line(self, widget):
		line_iter = self.buff.get_iter_at_line_offset((self.spin.get_value_as_int() - 1), 0)
		line = self.spin.get_value_as_int()-1

		if not (self.current_line is line):
			self.buff.place_cursor(line_iter)
			self.data.grab_focus()
			self.data.scroll_to_mark(self.buff.get_insert(), 0)
			
		self.w.hide_all()
		
	def spin_press(self, widget, key):
		if key.keyval == 65307:
			self.w.hide_all()
	
	def spin_release(self, widget, key):
		if key.keyval == 65293:
			self.switch_line(self)
		
	def hide_goto_line(self, widget):
		self.w.hide_all()

	def set_wrap(self, widget, action):
		i = 0
		for x in tab.editor_instance:
			tab.editor_instance.values()[i]._set_wrap_mode(widget.get_current_value())
			i = i + 1

	def set_scheme(self, widget, action):
		i = 0
		try:
			for x in tab.editor_instance:
				tab.editor_instance.values()[i]._set_scheme(widget.get_current_value())
				i = i + 1
			self.style = tab.editor_instance.values()[0].get_buffer().get_style_scheme()
		except:
			message = "Can't set Jollpi style"
			sec = "Download jollpi style at\nhttp://sourceforge.net/projects/jollpischeme/\nthen copy the jollpi.xml file which resides in the package to directory style of your gtksourceview library"
			tab.error_message("Error", message, self.parent, sec)

	def enable_auto_indent(self, widget):
		i = 0
		for x in tab.editor_instance:
			if widget.get_active():
				tab.editor_instance.values()[i]._set_auto_indent(1)
			else:
				tab.editor_instance.values()[i]._set_auto_indent(0)
			i = i + 1
	
	def show_line_numbers(self, widget):
		i = 0
		for x in tab.editor_instance:
			if widget.get_active():
				tab.editor_instance.values()[i]._set_show_line_numbers(1)
			else:
				tab.editor_instance.values()[i]._set_show_line_numbers(0)
			i = i + 1
			
	def show_line_marks(self, widget):
		i = 0
		for x in tab.editor_instance:
			if widget.get_active():
				tab.editor_instance.values()[i]._set_show_line_marks(1)
			else:
				tab.editor_instance.values()[i]._set_show_line_marks(0)
			i = i + 1
			
	def show_right_margin(self, widget):
		i = 0
		for x in tab.editor_instance:
			if widget.get_active():
				tab.editor_instance.values()[i]._set_show_right_margin(1)
			else:
				tab.editor_instance.values()[i]._set_show_right_margin(0)
			i = i + 1
			
	def select_font_clicked(self, widget):
		self.win = gtk.FontSelectionDialog("Font Selection")
		self.win.set_position(gtk.WIN_POS_CENTER_ALWAYS)
		self.win.set_transient_for(self.parent)
		self.win.cancel_button.connect("clicked", lambda w:self.win.destroy())
		self.win.ok_button.connect("clicked", self.font_selection_ok)
		current_font = self.data.current_font()
		self.win.set_font_name(current_font)
		self.win.run()
		
	def font_selection_ok(self, button):
		font = self.win.get_font_name()
		i = 0
		for x in tab.editor_instance:
			tab.editor_instance.values()[i].set_font(font)
			i = i + 1
	        self.win.destroy()

	def show_docs(self, widget):
		helps.show_doc(self.parent)
		
	def show_about(self, widget):
		helps.show_about(self.parent)
		
	def aneh(self, tu, tr, ct, cp):
		self.tu = tu
		self.tr = tr
		self.tct = ct
		self.tcp = cp