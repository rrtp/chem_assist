import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

app=Gtk.Application()
print(dir(app.props))
