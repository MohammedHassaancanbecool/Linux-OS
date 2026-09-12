#!/usr/bin/env python3
import subprocess
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

class Vault(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Drakonis Vault")
        self.set_default_size(760, 520)
        self.connect("destroy", Gtk.main_quit)
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12, margin=20)
        self.add(box)
        title = Gtk.Label()
        title.set_markup('<span size="xx-large" weight="bold" foreground="#00D9FF">Drakonis Vault</span>\n<span foreground="#A9BCE8">Local case workspace • SHA-256 integrity • sealed records</span>')
        title.set_halign(Gtk.Align.START); box.pack_start(title, False, False, 0)
        row = Gtk.Box(spacing=8); box.pack_start(row, False, False, 0)
        self.case = Gtk.Entry(placeholder_text="case-name")
        row.pack_start(self.case, True, True, 0)
        for label, command in [("Create", "create"), ("List", "list")]:
            b = Gtk.Button(label=label); b.connect("clicked", self.action, command); row.pack_start(b, False, False, 0)
        self.file = Gtk.FileChooserButton(title="Select evidence file", action=Gtk.FileChooserAction.OPEN)
        box.pack_start(self.file, False, False, 0)
        row2 = Gtk.Box(spacing=8); box.pack_start(row2, False, False, 0)
        for label, command in [("Add file", "add"), ("Status", "status"), ("Verify", "verify"), ("Seal case", "seal")]:
            b = Gtk.Button(label=label); b.connect("clicked", self.action, command); row2.pack_start(b, False, False, 0)
        self.output = Gtk.TextView(editable=False, monospace=True, wrap_mode=Gtk.WrapMode.WORD_CHAR)
        box.pack_start(self.output, True, True, 0)
        note = Gtk.Label(label="Sealing verifies every recorded hash and prevents additional changes. Use a new case for new material.")
        note.set_halign(Gtk.Align.START); note.set_line_wrap(True); box.pack_end(note, False, False, 0)

    def action(self, _button, command):
        case = self.case.get_text().strip()
        args = ["/usr/local/bin/drakonis-vault", command]
        if command in ("create", "list"): args += ([case] if command == "create" and case else [])
        else:
            if not case: return self.show("Enter a case name first")
            args.append(case)
            if command == "add":
                path = self.file.get_filename()
                if not path: return self.show("Select an evidence file first")
                args.append(path)
        try:
            result = subprocess.run(args, capture_output=True, text=True, timeout=20)
            self.show((result.stdout + result.stderr).strip() or "Completed")
        except Exception as exc: self.show(str(exc))

    def show(self, text):
        self.output.get_buffer().set_text(text)

Gtk.init([]); win = Vault(); win.show_all(); Gtk.main()
