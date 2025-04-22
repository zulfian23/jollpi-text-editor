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

| Action                 | Shortcut           |
|------------------------|--------------------|
| **New Document**       | Ctrl+N             |
| **Open File**          | Ctrl+O             |
| **Save**               | Ctrl+S             |
| **Save As**            | Ctrl+Shift+S       |
| **Print**              | Ctrl+P             |
| **Close File**         | Ctrl+W             |
| **Quit**               | Ctrl+Q             |
| **Undo**               | Ctrl+Z             |
| **Redo**               | Ctrl+Shift+Z       |
| **Cut**                | Ctrl+X             |
| **Copy**               | Ctrl+C             |
| **Paste**              | Ctrl+V             |
| **Select All**         | Ctrl+A             |
| **Delete**             | Delete             |
| **Find**               | Ctrl+F             |
| **Find Next**          | F3                 |
| **Find Previous**      | Shift+F3           |
| **Replace**            | Ctrl+R             |
| **Go to Line**         | Ctrl+G             |
| **Toggle Insert/Overwrite** | Insert        |
| **Toggle Auto Indent** | F8                 |
| **Toggle Line Numbers**| F11                |
| **Toggle Line Marks**  | F9                 |
| **Toggle Right Margin**| F7                 |
| **Select Font**        | F6                 |
| **Help**               | F1                 |

## 🚀 Version
**2.1.2 (alpha)**

> Only the latest version is uploaded in this repository.

## 📋 Changelog
**2.1.2 (alpha)**

See full changelog in [ChangeLog](ChangeLog)

## 📦 Installation

Run the provided script on any Linux-based system:

```bash
chmod +x install.sh
./install.sh
```

Make sure Python and GTK dependencies are installed. For details, see [INSTALL](INSTALL).

## 👨‍💻 Author

Zulfian

## 📄 License
See [LICENSE](LICENSE)
