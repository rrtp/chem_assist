import gi,sqlite3
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import pages

#custom gtk application class containing helpful definitions
class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.chem_assist_project.chem_assist")

        self.connect('activate',self.on_activate)
    def on_activate(self,app):
        print("activated")
        page=pages.welcome_page(application=app)
        page.present()

#Create an instance of Application
app=Application()
app.run(None)