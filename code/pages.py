import gi
gi.require_version("Gtk","4.0")
from gi.repository import Gtk

#folder for Css, user interface layout definition,database,pictures
css_dir="styles/"
ui_dir="ui_definitions/"
db_dir="databases/"
pics_dir="pictures/"

#load css
css_file_path=css_dir+"styles.css"
css_provider=Gtk.CssProvider.new()
css_provider.load_from_path(css_file_path)
#load db
current_db=db_dir+""

#number of windows of history to remember
window_history_limit=100
#window history
window_history=[]
def window_history_delete_old():
    del window_history[0]
if len(window_history) > window_history_limit:
    window_history_delete_old()

#close current page
def close_page_cls(obj,app):
    print("exiting..")
    app.get_active_window().close()
    if len(window_history)>0:
        window_history.pop()
def close_page(app):
    print("closing current page..")
    if len(window_history)>0:
        window_history.pop()
    app.get_active_window().close()
#open  page
def open_page(obj,page,app):
    close_page(app)
    window_history.append(page)
    win=page(application=app)
    win.present()

#header bar
class header_bar(Gtk.HeaderBar):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #buttons
        back_button=Gtk.Button.new_with_label("b")
        settings_page_button=Gtk.Button.new_with_label("s")
        #populate
        self.pack_start(back_button)
        self.pack_end(settings_page_button)

#welcome page
class welcome_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="welcome!")

        #create welcome text
        welcome_button=Gtk.Button.new_with_label("Welcome to Chemistry Assistant!")
        self.set_child(welcome_button)

        #button function
        welcome_button.connect('clicked',open_page,main_menu_page,self.get_application())

#settings page
class settings_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="settings")
        self.application=self.get_application()

#main menu page
class main_menu_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Chemistry assistant main page")
        self.application=self.get_application()

        #buttons
        reactions_button=Gtk.Button.new_with_label("Reactions")
        quiz_button=Gtk.Button.new_with_label("Quiz")
        quit_button=Gtk.Button.new_with_label("Quit")
        simulator_button=Gtk.Button.new_with_label("Simulate")

        #main menu buttons box
        main_menu_buttons_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        main_menu_buttons_box.set_valign(Gtk.Align.CENTER)
        main_menu_buttons_box.set_halign(Gtk.Align.CENTER)
        #buttons in box
        main_menu_buttons_box.append(reactions_button)
        main_menu_buttons_box.append(quiz_button)
        main_menu_buttons_box.append(simulator_button)
        main_menu_buttons_box.append(quit_button)
        self.set_child(main_menu_buttons_box)

        #button functions
        reactions_button.connect('clicked',open_page,reactions_display_page,self.application)
        quiz_button.connect('clicked',open_page,quiz_main_page,self.application)
        quit_button.connect('clicked',close_page_cls,self.application)
        simulator_button.connect('clicked',open_page,simulator_page,self.application)

#quiz page
class quiz_main_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Quiz main page")

#Reactions page
class reactions_display_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Reactions")

        reactions_page_header_bar=header_bar()
        self.set_titlebar(reactions_page_header_bar)
        #boxes
        reactions_list_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        reactions_page_bottom_panel_box=Gtk.Box.new(Gtk.Orientation.HORIZONTAL,10)
        self.set_child(reactions_list_box)
        self.set_child(reactions_page_bottom_panel_box)

        #box properties
        reactions_page_bottom_panel_box.set_valign(Gtk.Align.END)
        reactions_page_bottom_panel_box.set_halign(Gtk.Align.END)

        #columns
        # reactions_list=Gtk.ColumnView.new()
        # reactions_list_box.append(reactions_list)
        # reaction_list_name_column=Gtk.ColumnViewColumn.new("Name",Gtk.ListItemFactory())
        # reaction_lists.append_column()

        #bottom panel
        reactions_db_import_button=Gtk.Button.new_with_label("Import")
        reactions_db_export_button=Gtk.Button.new_with_label("Export")
        reactions_db_add_button=Gtk.Button.new_with_label("Add")

        reactions_page_bottom_panel_box.append(reactions_db_import_button)
        reactions_page_bottom_panel_box.append(reactions_db_export_button)
        reactions_page_bottom_panel_box.append(reactions_db_add_button)

#simulator page
class simulator_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Simulator")
        reaction_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,0)
