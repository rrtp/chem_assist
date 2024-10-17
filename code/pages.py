import gi
gi.require_version("Gtk","4.0")
from gi.repository import Gtk

#close current page
def close_page_cls(obj,app):
    print("exiting..")
    app.get_active_window().close()
def close_page(app):
    print("closing current page..")
    app.get_active_window().close()
#open  page
def open_page(obj,page,app):
    close_page(app)
    win=page(application=app)
    win.present()

#welcome page
class welcome_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="welcome!")

        #create welcome text
        welcome_button=Gtk.Button.new_with_label("Welcome to Chemistry Assistant!")
        self.set_child(welcome_button)

        #button function
        welcome_button.connect('clicked',open_page,main_menu_page,self.get_application())

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
        main_menu_buttons_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,0)
        main_menu_buttons_box.set_valign(Gtk.Align.CENTER)

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

        #box for reactions list
        reactions_list_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        self.set_child(reactions_list_box)
        #add list to box   
        reactions_list=Gtk.ColumnView.new(Gtk.SelectionModel.MultiSelection)
        reactions_list_box.append(reactions_list)
        #Columns for gtk list
        reaction_list_name_column=Gtk.ColumnViewColumn.new("Name",Gtk.ListItemFactory())
        reaction_lists.append_column()

        #Buttons, bottom panel
        reactions_page_bottom_panel_box=Gtk.Box.new(Gtk.Orientation.HORIZONTAL,10)
        self.set_child(reactions_page_bottom_panel_box)
        reactions_db_import_button=Gtk.Button.new_with_label("Import")
        reactions_db_import_button=Gtk.Button.new_with_label("Export")
        reactions_db_import_button=Gtk.Button.new_with_label("Add")
        reactions_db_import_button=Gtk.Button.new_with_label("Import")

#simulator page
class simulator_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Simulator")
