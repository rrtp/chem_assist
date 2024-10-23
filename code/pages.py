import gi
gi.require_version("Gtk","4.0")
from gi.repository import Gtk,Gio,GObject

#header bar
def set_css_class_to_child(parent,css_class):
    children=[]
    children.append(parent.get_first_child())
    i=children[-1]
    while i!=None:
        children[-1].add_css_class(css_class)
        i=children[-1].get_next_sibling()
        children.append(i)
class settings_button(Gtk.Button):
    def __init__(self,icon,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_child(icon)
class header_bar(Gtk.HeaderBar):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    def set_titlebar(self,page,settings=True,back_button=True):
        page.set_titlebar(self())
        if settings==True:
            #set settings button and connect to settings page
            self.settings_button=settings_button(page.props.application.settings_image)
            page.props.titlebar.pack_end(page.props.titlebar.settings_button)
            page.props.titlebar.settings_button.connect('clicked',page.props.application.open_page,settings_page)
        if back_button==True:
            self.back_button=Gtk.Button.new_with_label("b")
            page.props.titlebar.back_button.connect('clicked',page.props.application.open_page,page.props.application.window_history[-2])
            page.props.titlebar.pack_start(page.props.titlebar.back_button)

#welcome page
class welcome_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="welcome!")
        #event controller
        event_controller=Gtk.EventControllerKey()
        self.add_controller(event_controller)
        #welcome message
        welcome_message=Gtk.Label.new()
        self.set_child(welcome_message)
        welcome_message.set_markup(\
            """<span font-size='50pt'>Welcome to Chemistry assistant!</span>
            <span>\n\n\n\n\n\n\n</span>
            <span font-size="20pt">Press any key to start!</span>""")
        #event controller function
        event_controller.connect('key-pressed',self.do_key_pressed)
    def do_key_pressed(self,*args):
        for i in args:
            print(i)
        print("key pressed")
        self.props.application.open_page(None,main_menu_page)
#settings page
class settings_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="settings")
        header_bar.set_titlebar(header_bar,self,settings=False)
#main menu page
class main_menu_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Chemistry assistant main page")
        self.props.name="main_menu_page"
        self.add_css_class("main_manu_page")
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

        #css
        main_menu_buttons_box.add_css_class("main_menu_buttons_box")
        set_css_class_to_child(main_menu_buttons_box,"main_menu_buttons_box")

        #button functions
        reactions_button.connect('clicked',self.props.application.open_page,reactions_display_page)
        quiz_button.connect('clicked',self.props.application.open_page,quiz_main_page)
        quit_button.connect('clicked',self.props.application.close_page)
        simulator_button.connect('clicked',self.props.application.open_page,simulator_page)

#quiz page
class quiz_main_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Quiz main page")
        header_bar.set_titlebar(header_bar,self)

class reactions_list(GObject.Object):
    def __init__(self,name,reactant,product,extra_info):
        super().__init__()
        self.name=name
        self.reactant=reactant
        self.product=product
        self.extra_info=extra_info
#Reactions page
class reactions_display_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Reactions")

        header_bar.set_titlebar(header_bar,self)
        #boxes
        reactions_page_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        reactions_page_box.set_homogeneous(True)
        self.set_child(reactions_page_box)

        reactions_list_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        reactions_page_bottom_panel_box=Gtk.Box.new(Gtk.Orientation.HORIZONTAL,10)

        reactions_page_box.append(reactions_list_box)
        reactions_page_box.append(reactions_page_bottom_panel_box)

        #box properties
        reactions_page_bottom_panel_box.set_valign(Gtk.Align.END)
        reactions_page_bottom_panel_box.set_halign(Gtk.Align.END)

        #list panel
        #model
        self.reactions_list=Gio.ListStore.new(reactions_list)
        self.reactions_list_multiselection=Gtk.MultiSelection.new(self.reactions_list)

        #columns
        name_column_signal_tracker=Gtk.SignalListItemFactory.new()
        name_column=Gtk.ColumnViewColumn.new("name",name_column_signal_tracker)

        reactants_column_signal_tracker=Gtk.SignalListItemFactory.new()
        reactants_column=Gtk.ColumnViewColumn.new("name",reactants_column_signal_tracker)

        products_column_signal_tracker=Gtk.SignalListItemFactory.new()
        products_column=Gtk.ColumnViewColumn.new("name",products_column_signal_tracker)

        extra_info_column_signal_tracker=Gtk.SignalListItemFactory.new()
        extra_info_column=Gtk.ColumnViewColumn.new("name",extra_info_column_signal_tracker)

        #bottom panel
        reactions_db_import_button=Gtk.Button.new_with_label("Import")
        reactions_db_export_button=Gtk.Button.new_with_label("Export")
        reactions_db_add_button=Gtk.Button.new_with_label("Add")

        reactions_page_bottom_panel_box.append(reactions_db_import_button)
        reactions_page_bottom_panel_box.append(reactions_db_export_button)
        reactions_page_bottom_panel_box.append(reactions_db_add_button)   

class simulator_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Simulator")
        header_bar.set_titlebar(header_bar,self)
        reaction_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,0)
