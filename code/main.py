import gi,sqlite3
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk
import pages

#folder for Css, user interface layout definition,database,pictures
css_dir="styles/"
ui_dir="ui_definitions/"
db_dir="databases/"
pics_dir="pictures/"

#load css
css_file_path=css_dir+"styles.css"
css_provider=Gtk.CssProvider.new()
css_provider.load_from_path(css_file_path)
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(),css_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
#load db
current_db=db_dir+""

#window history
window_history=[]

#custom gtk application class containing helpful definitions
class Application(Gtk.Application):
    window_history=window_history
    def __init__(self):
        super().__init__(application_id="com.chem_assist_project.chem_assist")
        self.connect('activate',self.on_activate)

    def on_activate(self,app):
        print("activated")
        self.open_page(None,pages.welcome_page)
    #close current page
    def close_page(self,caller_obj=None,page=None):
        print("closing current page..",window_history)
        if page!=None:
            page.close()
        if page==None and self.get_active_window()!=None:
            self.props.active_window.close()
    #open page
    def open_page(app,caller_obj,page):
        app.close_page(page=app.props.active_window)
        app.window_history.append(page)
        page=page(application=app)
        page.present()

#Create an instance of Application
app=Application()
app.run(None)