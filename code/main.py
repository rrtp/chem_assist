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
        win=welcome_window(application=app)
        win.present()
        print(win.get_css_name())


class welcome_window(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.set_css_name("welcome_window")
        self.set_title("Welcome!")

        #create welcome text
        welcome_text=Gtk.Label.new("Welcome to Chemistry Assistant!")
        self.set_child(welcome_text)

class main_menu_window(Gtk.ApplicationWindow):
    def __init__():
        super().init()

        self.set_title("Chemistry assistant main page")

        #buttons
        reactions_button=Gtk.Button.new_with_label("Reactions")
        self.set_child(reactions_button)
        quiz_button=Gtk.Button.new_with_label("Quiz")
        self.set_child(quiz_button)

        #main menu buttons box
        main_menu_buttons_box=Gtk.Box.new(Gtk.orientation.VERTICAL,0)
        main_menu_buttons_box.append(reactions_button)
        main_menu_buttons_box.append(quiz_button)
        self.set_child(main_menu_buttons_box)

#Create an instance of Application
app=Application()
app.run(None)