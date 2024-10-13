import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

#folder for Css, user interface layout definition files
css_dir="styles/"
ui_dir="ui_definitions/"

css_file_path=css_dir+"styles.css"
#create an empty css provider and load css styles in css file present in the file path into css provider
css_provider=Gtk.CssProvider.new()
css_provider.load_from_path(css_file_path)

#custom gtk application class containing helpful definitions
class Application(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.chem_assist_project.chem_assist")
        self.connect('activate',self.on_activate)
    def on_activate(self,app):
        print("activated")

#define the ui file name, create gtk builder instance
ui_file_path=ui_dir+"interface.ui"
gtk_builder=Gtk.Builder.new_from_file(ui_file_path)
print(gtk_builder.get_objects())

#Create an instance of Application
app=Application()
app.run(None)