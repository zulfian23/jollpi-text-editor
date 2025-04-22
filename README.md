# Jollpi

**Jollpi** is a lightweight, feature-rich text editor built using Python and GTK. Originally developed as a college final project in 2010, Jollpi is designed to be simple, fast, and useful for programmers working on Linux systems.

![screenshot](screenshot.png)

## ✨ Features

- Tabbed interface for multiple documents
- Syntax highlighting for C/C++, Java, Python, Perl, Bash, and more (using GtkSourceView)
- File modification detection (external changes)
- Find, Find Next/Previous, Replace, and Go to Line
- Auto indent, line numbers, line marks, and right margin display
- Font customization (family, size, style)
- Print and page setup support
- Wrap mode and theme switching
- Full undo/redo, clipboard support (cut/copy/paste)
- Accessible via command line:  
  ```bash
  jollpi
  ```

## 🧭 Interface Overview
- Menubar – Full command access
- Toolbar – Quick access to frequently used actions
- Display area – The main editor window
- Statusbar – Shows cursor position, edit mode (INS/OVR), and contextual info

## ⌨️ Keyboard Shortcuts

Action | Shortcut
New | Ctrl+N
Open | Ctrl+O
Save | Ctrl+S
Save As | Ctrl+Shift+S
Print | Ctrl+P
Quit | Ctrl+Q
Undo / Redo | Ctrl+Z / Ctrl+Shift+Z
Cut / Copy / Paste | Ctrl+X / Ctrl+C / Ctrl+V
Select All / Delete | Ctrl+A / Delete
Find / Replace | Ctrl+F / Ctrl+R
Find Next / Prev | F3 / Shift+F3
Go to Line | Ctrl+G
Toggle Wrap | -
Auto Indent | F8
Line Numbers | F11
Line Marks | F9
Right Margin | F7
Select Font | F6
Help / About | F1 / -

Insert key toggles between Insert and Overwrite mode.

## 🚀 Version

**2.1.2 (alpha)**
Note: This is the only version available in this repository. Older versions are not included.

## 📋 Changelog
2.1.2 (alpha)
Fixed compatibility issue with Python 2.6

Fixed icon/image loading bugs

Updated installer to support uninstall process

See full changelog in [ChangeLog](ChangeLog)

## 📦 Installation

Run the provided script on any Linux-based system:

```bash
bash install.sh
```

Make sure Python and GTK dependencies are installed. For details, see [INSTALL](INSTALL).

## 👨‍💻 Author

Zulfian

## 📄 License
See [LICENSE](LICENSE)
