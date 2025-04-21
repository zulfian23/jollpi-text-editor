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
import subprocess

PROGRAMNAME = "JOLLPI"
RELEASE="1"
REVISION="2"
VERSION = "2.%s.%s" %(RELEASE, REVISION)
COPYRIGHT = "Copyright (c) 2010 The JOLLPI Author"
EMAIL = "fianmyung@gmail.com"
YM = "baxilisk_07"
AUTHOR ="Zulfian <%s> [YM: %s]" % (EMAIL, YM)
author = [AUTHOR]

gpl = """
Copyright (c) 2010 Zulfian <fianmyung@gmail.com>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""

class Help:
	def show_about(self, window):
		dialog = gtk.AboutDialog()
		dialog.set_transient_for(window)
		dialog.set_name(PROGRAMNAME)
		dialog.set_version(VERSION)
		dialog.set_copyright(COPYRIGHT)
		dialog.set_comments("Jollpi is a simple but usefull text editor")
		dialog.set_license(gpl)
		dialog.set_authors(author)
		dialog.set_documenters(author)
		try:
			pixbuf = gtk.gdk.pixbuf_new_from_file('/usr/share/pixmaps/jollpi.png')
		except:
			pixbuf = gtk.gdk.pixbuf_new_from_file('/usr/local/share/pixmaps/jollpi.png')

		dialog.set_logo(pixbuf)

		dialog.run()
		dialog.destroy()
		
	def show_doc(self, window):
		browser = ["firefox", "google-chrome", "khelpcenter", "konqueror", "yelp"]
		file = "/usr/share/doc/jollpi/index.html"
		file1 = "/usr/local/share/doc/jollpi/index.html"
		for x in browser:
			try:
				try:
					op = open(file, "rb")
					op.close()
					subprocess.Popen([x, file]).pid
					break
				except:
					subprocess.Popen([x, file1]).pid
					break
			except:
				pass
		else:
			message = "Can't launch help browser"
			sec_message = """
Please install one of the browsers listed below :
1. Konqueror
2. KDE Help Center
3. Mozilla Firefox
4. Yelp
5. Google Chrome
 
You can also open it manually with your own browser in
'/usr/share/doc/jollpi/index.html' or '/usr/local/share/doc/jollpi/index.html'"""
			
			msg = gtk.MessageDialog(window, 0, gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
			msg.set_title("Jollpi")
			msg.format_secondary_text(sec_message)
			msg.run()
			msg.destroy()
