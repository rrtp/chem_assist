import gi,sqlite3
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk
import pages

#uncomment to set dark theme
#Gtk.Settings.get_default().set_property('gtk_application_prefer_dark_theme',True)

#folder for Css, user interface layout definition,database,pictures
css_dir="styles/"
ui_dir="ui_definitions/"
db_dir="databases/"
pics_dir="pictures/"

#picstures paths
image_paths={
    "settings":pics_dir+"settings.svg",
    "back":pics_dir+"back.svg",
    "app":pics_dir+"app_image.svg"
}

#css file path
css_file_path=css_dir+"styles.css"

#db path
current_db=db_dir+""

#custom gtk application class containing helpful definitions
class Application(Gtk.Application):
    #window history
    window_history_limit=10
    window_history=[]

    #default display
    default_display=Gdk.Display.get_default()
    primary_monitor=default_display.get_monitors()[0]
    monitor_geometry=primary_monitor.get_geometry()
    monitor_width=monitor_geometry.width
    monitor_height=monitor_geometry.height

    #images
    settings_image=Gtk.Image.new_from_resource(image_paths["settings"])
    back_image=Gtk.Image.new_from_resource(image_paths["back"])
    app_image=Gtk.Image.new_from_resource(image_paths["app"])

    #constructor
    def __init__(self):
        super().__init__(application_id="com.chem_assist_project.chem_assist")
        self.connect('activate',self.on_activate)
        self.add_styles()
    def on_activate(self,app):
        print("activated")
        self.open_page(None,pages.welcome_page)
    
    #close current page
    def close_page(self,caller_obj=None,page=None):
        print("closing current page..",self.window_history)
        if page!=None:
            page.close()
        if page==None and self.get_active_window()!=None:
            self.props.active_window.close()
    #open page
    def open_page(app,caller_obj,page):
        app.close_page(page=app.props.active_window)

        app.window_history.append(page)
        app.window_history_size=len(app.window_history)
        if app.window_history_size > 3 and app.window_history[-1] == app.window_history[-3]:
            app.window_history.pop()
            app.window_history.pop()
        if app.window_history_size>app.window_history_limit:
            del app.window_history[0]

        page=page(application=app)
        page.set_default_size(app.monitor_width/2,app.monitor_height/2)
        page.present()
    
    def add_styles(self):
        #load css
        css_provider=Gtk.CssProvider.new()
        css_provider.load_from_path(css_file_path)
        Gtk.StyleContext.add_provider_for_display(self.default_display,css_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

#Create an instance of Application
app=Application()
app.run(None)