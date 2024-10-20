import gi
gi.require_version("Gtk","4.0")
from gi.repository import Gtk

#setting window names
page_names={}
page_names["main_menu_page"]="main_menu_page"

#header bar
class header_bar(Gtk.HeaderBar):
    #buttons
    back_button=Gtk.Button.new_with_label("b")
    settings_button=Gtk.Button.new_with_label("s")
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        #populate
        self.pack_start(self.back_button)

def set_titlebar(page,titlebar=header_bar,settings=True,back_button=True):
    page.set_titlebar(titlebar())
    if settings==True:
        #set settings button and connect to settings page
        page.props.titlebar.settings_button=Gtk.Button.new_with_label("s")
        page.props.titlebar.settings_button.connect('clicked',page.props.application.open_page,settings_page)
        page.props.titlebar.pack_end(page.props.titlebar.settings_button)
    if back_button==True:
        pass
#welcome page
class welcome_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="welcome!")

        #create welcome text
        welcome_button=Gtk.Button.new_with_label("Welcome to Chemistry Assistant!")
        self.set_child(welcome_button)

        #button function
        welcome_button.connect('clicked',self.props.application.open_page,main_menu_page)

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
        self.props.name=page_names["main_menu_page"]
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
        reactions_button.connect('clicked',self.application.open_page,reactions_display_page)
        quiz_button.connect('clicked',self.application.open_page,quiz_main_page)
        quit_button.connect('clicked',self.application.close_page)
        simulator_button.connect('clicked',self.application.open_page,simulator_page)

#quiz page
class quiz_main_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Quiz main page")

#Reactions page
class reactions_display_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Reactions")

        reactions_page_header_bar=header_bar()
        reactions_page_header_bar.settings_button.connect('clicked',self.props.application.open_page,settings_page)
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
