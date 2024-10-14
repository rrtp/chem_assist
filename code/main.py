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

#welcome window
class welcome_window(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.set_css_name("welcome_window")
        self.set_title("Welcome!")

        #create welcome text
        welcome_button=Gtk.Button.new_with_label("Welcome to Chemistry Assistant!")
        self.set_child(welcome_button)
        welcome_button.connect('clicked',self.on_click)

    def on_click(self,button):
        self.close()
        win=main_menu_window(application=app)
        win.present()

#fallback class if no obj arg is present
class fallback():
    def get_label():
        return "no button"
#close current window
def close_win(obj=fallback,*args):
    print(obj.get_label()," button selected, exiting..")
    app.get_active_window().close()
#open quiz window
def open_quiz_main_page_win(*args,**kwargs):
    app.get_active_window().close()
    win=quiz_main_page_win(application=app)
    win.present()
#open reactions page
def open_reactions_display_win(*args,**kwargs):
    app.get_active_window().close()
    win=reactions_display_win(application=app)

#main menu window
class main_menu_window(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.set_title("Chemistry assistant main page")

        #buttons
        reactions_button=Gtk.Button.new_with_label("Reactions")
        quiz_button=Gtk.Button.new_with_label("Quiz")
        quit_button=Gtk.Button.new_with_label("Quit")

        #main menu buttons box
        main_menu_buttons_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,0)
        main_menu_buttons_box.append(reactions_button)
        main_menu_buttons_box.append(quiz_button)
        main_menu_buttons_box.append(quit_button)
        self.set_child(main_menu_buttons_box)

        #button functions
        reactions_button.connect('clicked',open_reactions_display_win)
        quiz_button.connect('clicked',open_quiz_main_page_win)
        quit_button.connect('clicked',close_win)

class reactions_display_win(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.set_title("Reactions")

class quiz_main_page_win(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
        self.set_title("Quiz main page")
#Create an instance of Application
app=Application()
app.run(None)