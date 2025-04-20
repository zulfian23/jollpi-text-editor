#!/usr/bin/python

from distutils.core import setup

_data_files = [
	('share/applications', ['jollpi/share/jollpi.desktop']),
	('share/pixmaps', ['jollpi/share/apple-red.png']),
	('share/pixmaps', ['jollpi/share/apple-green.png']),
	('share/pixmaps', ['jollpi/share/jollpi.png']),
	('share/doc/jollpi', ['jollpi/helps/index.html']),
	('share/doc/jollpi', ['jollpi/helps/intro.html']),
	('share/doc/jollpi', ['jollpi/helps/getstarted.html']),
	('share/doc/jollpi', ['jollpi/helps/shortcut.html']),
	('share/doc/jollpi', ['jollpi/helps/credit.html']),
	('share/doc/jollpi', ['jollpi/helps/fdl-1.2.txt']),
	('share/doc/jollpi', ['jollpi/helps/menu.html']),
	('share/doc/jollpi', ['jollpi/helps/figure1.png']),
	]

files = ["MainEditor/__init__.py",
	"MainEditor/menubar.py",
	"MainEditor/toolbar.py",
	"MainEditor/notebook.py",
	"MainEditor/editor.py",
	"MainEditor/statusbar.py",
	"MainEditor/help.py",
	"docs/ChangeLog",
	"docs/LICENSE"
]

setup(
	name = 'jollpi',
	version = '2.1.2',
	description = 'Simple but usefull text editor',
	author = 'Zulfian',
	author_email = 'fianmyung@gmail.com',
	license = 'GPL',
    	packages = ['jollpi'],
	package_data = {'jollpi' : files },
	scripts = ['jollpi/jollpi'],
	data_files = _data_files,
)

