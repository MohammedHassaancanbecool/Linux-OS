#!/usr/bin/env python3
import os
import subprocess
import threading
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib, Gdk

ACCENT = "#00D9FF"
VIOLET = "#7B3FF2"
BG = "#0B1224"
CARD = "#101A35"
TEXT = "#F2F6FF"
MUTED = "#A9BCE8"

PAGES = [
    ("desktop", "Desktop", "Desktop overview and workspace shortcuts"),
    ("applications", "Applications", "Search and launch installed tools"),
    ("files", "File Manager", "Open files and navigate the workspace"),
    ("security", "Security Center", "Isolation, firewall, updates, and local health"),
    ("network", "Network Tools", "Interfaces, routes, DNS, and local sockets"),
    ("monitor", "System Monitor", "CPU, memory, storage, and processes"),
    ("notifications", "Notifications", "Recent events and quick actions"),
    ("workspaces", "Workspace Overview", "Organize tasks across four workspaces"),
    ("settings", "Settings Center", "Appearance, keyboard, display, and devices"),
    ("themes", "Themes Manager", "Choose Night or Carbon visual themes"),
    ("software", "Software Center", "Review profiles and package sources"),
    ("browser", "Web Browser", "Open the browser with privacy guidance"),
    ("code", "Code Editor", "Open a development workspace"),
    ("first", "First Run", "Review the safe-by-default lab setup"),
    ("help", "Help Center", "Safety guide, shortcuts, and documentation"),
    ("power", "Power & Session", "Lock, suspend, log out, restart, or shut down"),
    ("evidence", "Case Workspace", "Create cases, hash evidence, verify, and seal records"),
]

class DrakonisCenter(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Drakonis Control Center")
        self.set_default_size(1180, 760)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("destroy", Gtk.main_quit)
        self.apply_css()
        root = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        root.get_style_context().add_class("root")
        self.add(root)
        sidebar = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        sidebar.set_size_request(250, -1)
        sidebar.get_style_context().add_class("sidebar")
        root.pack_start(sidebar, False, False, 0)
        brand = Gtk.Label()
        brand.set_markup('<span size="x-large" weight="bold" foreground="#00D9FF">DRAKONIS</span>\n<span foreground="#A9BCE8">Control Center</span>')
        brand.set_halign(Gtk.Align.START)
        brand.set_margin_top(24); brand.set_margin_start(22); brand.set_margin_bottom(16)
        sidebar.pack_start(brand, False, False, 0)
        search = Gtk.SearchEntry(placeholder_text="Search screens…")
        search.set_margin_start(16); search.set_margin_end(16); search.set_margin_bottom(8)
        search.connect("search-changed", self.filter_pages)
        sidebar.pack_start(search, False, False, 0)
        self.page_buttons = []
        for key, title, _ in PAGES:
            button = Gtk.Button(label=title)
            button.set_halign(Gtk.Align.FILL)
            button.set_margin_start(12); button.set_margin_end(12)
            button.set_relief(Gtk.ReliefStyle.NONE)
            button.connect("clicked", self.show_page, key)
            sidebar.pack_start(button, False, False, 0)
            self.page_buttons.append((button, title.lower()))
        sidebar.pack_end(Gtk.Label(label="Authorized defensive analysis only"), False, False, 18)
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        root.pack_start(content_box, True, True, 0)
        self.header = Gtk.Label()
        self.header.set_halign(Gtk.Align.START)
        self.header.set_margin_top(26); self.header.set_margin_start(34); self.header.set_margin_bottom(14)
        content_box.pack_start(self.header, False, False, 0)
        self.stack = Gtk.Stack(transition_type=Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        self.stack.set_margin_start(30); self.stack.set_margin_end(30); self.stack.set_margin_bottom(30)
        content_box.pack_start(self.stack, True, True, 0)
        for key, title, description in PAGES:
            self.stack.add_named(self.make_page(key, title, description), key)
        self.show_page(None, "desktop")

    def apply_css(self):
        css = Gtk.CssProvider()
        css.load_from_data(f"""
        .root {{ background: {BG}; color: {TEXT}; }}
        .sidebar {{ background: #07111F; border-right: 1px solid #283B9F; }}
        button {{ background: {CARD}; color: {TEXT}; border: 1px solid #283B9F; border-radius: 7px; padding: 10px; }}
        button:hover, button:checked {{ background: #283B9F; border-color: {ACCENT}; }}
        entry, searchentry {{ background: #101A35; color: {TEXT}; border: 1px solid #283B9F; border-radius: 6px; }}
        .card {{ background: {CARD}; border: 1px solid #283B9F; border-radius: 10px; padding: 18px; }}
        .accent {{ color: {ACCENT}; }}
        label {{ color: {TEXT}; }}
        """.encode())
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def filter_pages(self, entry):
        text = entry.get_text().lower()
        for button, title in self.page_buttons:
            button.set_visible(not text or text in title)

    def make_page(self, key, title, description):
        page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        intro = Gtk.Label()
        intro.set_markup(f'<span size="xx-large" weight="bold">{title}</span>\n<span foreground="{MUTED}">{description}</span>')
        intro.set_halign(Gtk.Align.START)
        page.pack_start(intro, False, False, 0)
        grid = Gtk.Grid(column_spacing=16, row_spacing=16)
        page.pack_start(grid, False, False, 0)
        if key == "security":
            self.card(grid, 0, 0, "Isolation", "Check or enable loopback-only output.", "mll-network-isolation status", "/usr/local/bin/mll-network-isolation status")
            self.card(grid, 1, 0, "Firewall", "Inspect local nftables rules.", "View rules", "nft list ruleset")
            self.card(grid, 0, 1, "Updates", "Use Debian repositories and review transactions.", "Open profile installer", "/usr/local/bin/drakonis-install-profile")
            self.card(grid, 1, 1, "Release", "Show image metadata.", "mll-release", "mll-release")
        elif key == "network":
            self.card(grid, 0, 0, "Interfaces", "Local interfaces and addresses.", "Inspect", "ip -brief address")
            self.card(grid, 1, 0, "Routes", "Local routing table.", "Inspect", "ip route")
            self.card(grid, 0, 1, "DNS", "Configured resolver status.", "Inspect", "cat /etc/resolv.conf")
            self.card(grid, 1, 1, "Sockets", "Listening local services.", "Inspect", "ss -lntup")
        elif key == "themes":
            self.card(grid, 0, 0, "DRAKONIS-Night", "Indigo, Cyan, and Violet.", "Apply Night", "xfconf-query -c xsettings -p /Net/ThemeName -s DRAKONIS-Night")
            self.card(grid, 1, 0, "DRAKONIS-Carbon", "Graphite, Teal, and cool white.", "Apply Carbon", "xfconf-query -c xsettings -p /Net/ThemeName -s DRAKONIS-Carbon")
        elif key == "power":
            self.card(grid, 0, 0, "Lock Screen", "Protect the current session.", "Lock", "xflock4")
            self.card(grid, 1, 0, "Suspend", "Pause the VM or workstation.", "Suspend", "systemctl suspend")
            self.card(grid, 0, 1, "Log Out", "End the XFCE session.", "Log out", "xfce4-session-logout --logout")
            self.card(grid, 1, 1, "Restart / Shut Down", "Requires an explicit confirmation.", "Open safe menu", "/usr/local/bin/drakonis-power-session")
        elif key == "applications":
            self.card(grid, 0, 0, "Tool Profiles", "Install Debian-native authorized profiles.", "Open installer", "/usr/local/bin/drakonis-install-profile")
            self.card(grid, 1, 0, "Red Team", "Optional adversary-simulation profile for owned labs.", "Open help", "/usr/local/bin/drakonis-help-center")
        elif key == "files":
            self.card(grid, 0, 0, "Home", "Open your analyst workspace.", "Open", "thunar")
            self.card(grid, 1, 0, "File safety", "Use snapshots before examining untrusted files.", "Read guide", "/usr/local/bin/drakonis-help-center")
        elif key == "browser":
            self.card(grid, 0, 0, "Firefox ESR", "Privacy-aware browsing for research.", "Open browser", "firefox-esr")
            self.card(grid, 1, 0, "Lab boundary", "Do not connect untrusted production accounts.", "Read guide", "/usr/local/bin/drakonis-help-center")
        elif key == "code":
            self.card(grid, 0, 0, "Terminal workspace", "Use tmux, Vim, and Python tools.", "Open terminal", "xfce4-terminal")
            self.card(grid, 1, 0, "Documentation", "Keep scope and evidence notes local.", "Open help", "/usr/local/bin/drakonis-help-center")
        elif key == "evidence":
            self.card(grid, 0, 0, "Drakonis Vault", "Manage local case folders and SHA-256 manifests.", "Open vault", "/usr/local/bin/drakonis-vault-ui")
            self.card(grid, 1, 0, "Integrity", "Verify recorded hashes before sealing a case.", "Open vault", "/usr/local/bin/drakonis-vault-ui")
        elif key == "software":
            self.card(grid, 0, 0, "Profiles", "List Debian-native security profiles.", "List profiles", "/usr/local/bin/drakonis-software-center profiles")
            self.card(grid, 1, 0, "Package lookup", "Inspect a package without installing it.", "Open center", "/usr/local/bin/drakonis-software-center")
            self.card(grid, 0, 1, "Repository policy", "Only configured Debian repositories are allowed.", "Show policy", "apt-cache policy")
        elif key == "monitor":
            self.card(grid, 0, 0, "CPU and memory", "Live local resource snapshot.", "Inspect", "uptime; free -h")
            self.card(grid, 1, 0, "Storage", "Filesystem usage for the analyst workspace.", "Inspect", "df -h /")
            self.card(grid, 0, 1, "Processes", "Review local processes without target activity.", "Inspect", "ps -eo pid,comm,%cpu,%mem --sort=-%cpu | head -n 16")
        elif key == "notifications":
            self.card(grid, 0, 0, "Recent events", "Review local journal warnings and service events.", "Open journal", "journalctl -b -p warning..alert --no-pager -n 30")
            self.card(grid, 1, 0, "Safety notice", "No automatic target discovery is performed.", "Open help", "/usr/local/bin/drakonis-help-center")
        elif key == "workspaces":
            self.card(grid, 0, 0, "Workspace 1", "Primary analyst desktop.", "Switch", "wmctrl -s 0")
            self.card(grid, 1, 0, "Workspace 2", "Evidence and notes.", "Switch", "wmctrl -s 1")
            self.card(grid, 0, 1, "Workspace 3", "Tool execution.", "Switch", "wmctrl -s 2")
            self.card(grid, 1, 1, "Workspace 4", "Review and reporting.", "Switch", "wmctrl -s 3")
        elif key == "settings":
            self.card(grid, 0, 0, "Appearance", "Open XFCE appearance settings.", "Open", "xfce4-appearance-settings")
            self.card(grid, 1, 0, "Display", "Configure displays and scaling.", "Open", "xfce4-display-settings")
            self.card(grid, 0, 1, "Keyboard", "Configure shortcuts and layout.", "Open", "xfce4-keyboard-settings")
            self.card(grid, 1, 1, "Session", "Review startup applications.", "Open", "xfce4-session-settings")
        else:
            self.card(grid, 0, 0, "Ready", "This Drakonis workspace is safe-by-default and keyboard friendly.", "Open Help Center", "/usr/local/bin/drakonis-help-center")
            self.card(grid, 1, 0, "Next step", "Use isolated networking and a disposable VM snapshot.", "Open First Run", "/usr/local/bin/drakonis-first-run")
        note = Gtk.Label(label="No automatic target discovery is performed. Use all tools only within written authorization.")
        note.set_halign(Gtk.Align.START); note.set_margin_top(12)
        note.get_style_context().add_class("accent")
        page.pack_end(note, False, False, 0)
        return page

    def card(self, grid, col, row, title, desc, button_text, command):
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        box.set_size_request(380, 120); box.get_style_context().add_class("card")
        label = Gtk.Label(); label.set_markup(f'<span size="large" weight="bold">{title}</span>\n<span foreground="{MUTED}">{desc}</span>'); label.set_halign(Gtk.Align.START)
        box.pack_start(label, True, True, 0)
        button = Gtk.Button(label=button_text); button.connect("clicked", lambda *_: self.run_command(command)); box.pack_end(button, False, False, 0)
        grid.attach(box, col, row, 1, 1)

    def run_command(self, command):
        def worker():
            try:
                result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=15)
                text = (result.stdout + result.stderr).strip() or "Command completed."
            except Exception as exc:
                text = str(exc)
            GLib.idle_add(self.show_result, text)
        threading.Thread(target=worker, daemon=True).start()

    def show_result(self, text):
        dialog = Gtk.MessageDialog(transient_for=self, flags=0, message_type=Gtk.MessageType.INFO, buttons=Gtk.ButtonsType.OK, text="Drakonis result")
        dialog.format_secondary_text(text[:4000])
        dialog.run(); dialog.destroy(); return False

    def show_page(self, _button, key):
        for button, _ in self.page_buttons:
            button.set_active(False)
        self.stack.set_visible_child_name(key)
        title = dict((k, t) for k, t, _ in PAGES)[key]
        self.header.set_markup(f'<span foreground="{ACCENT}" size="large">{title}</span>  <span foreground="{MUTED}">Drakonis Linux v0.4.0</span>')

Gtk.init([])
window = DrakonisCenter()
window.show_all()
Gtk.main()
