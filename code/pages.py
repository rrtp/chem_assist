import gi
gi.require_version("Gtk","4.0")
from gi.repository import Gtk,Gio,GObject

def get_children(parent):
    children=[]
    children.append(parent.get_first_child())
    while True:
        sibling=children[-1].get_next_sibling()
        if sibling==None:
            break
        children.append(sibling)
    return children
def add_css_class_to_children(parent,css_class):
    children=get_children(parent)
    for i in children:
        i.add_css_class(css_class)
class settings_button(Gtk.Button):
    def __init__(self,icon,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.set_child(icon)

#header bar        
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
            self.settings_button.add_css_class("headerbar")
        if back_button==True:
            self.back_button=Gtk.Button.new_with_label("b")
            page.props.titlebar.back_button.connect('clicked',page.props.application.open_page,page.props.application.window_history[-2])
            page.props.titlebar.pack_start(page.props.titlebar.back_button)
            self.back_button.add_css_class("headerbar")

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
            f"""<span font-size='{self.props.application.monitor_width/50}pt'>Welcome to Chemistry assistant!</span>
            <span>{"\n"*int(self.props.application.monitor_height/50)}</span>
            <span font-size="{self.props.application.monitor_width/120}pt">Press any key to start!</span>""")
        #event controller function
        event_controller.connect('key-pressed',self.do_key_pressed)
    def do_key_pressed(self,*args):
        self.props.application.open_page(None,main_menu_page)

#settings page
class settings_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="settings")
        header_bar.set_titlebar(header_bar,self,settings=False)

        self.main_box=Gtk.Box.new(Gtk.Orientation.HORIZONTAL,0)
        self.set_child(self.main_box)

        side_panel_scroll=Gtk.ScrolledWindow.new()
        side_panel_scroll.set_propagate_natural_width(True)
        settings_categories_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,0)
        side_panel_scroll.set_child(settings_categories_box)

        self.settings_box=Gtk.Box.new(Gtk.Orientation.HORIZONTAL,0)
        self.settings_box.set_hexpand(True)

        self.main_box.append(side_panel_scroll)
        self.main_box.append(self.settings_box)

        appearance_settings_button=Gtk.Button.new_with_label("Appearance")
        db_settings_button=Gtk.Button.new_with_label("Database")
        users_settings_button=Gtk.Button.new_with_label("Users")

        settings_categories_box.append(appearance_settings_button)
        settings_categories_box.append(db_settings_button)
        settings_categories_box.append(users_settings_button)
        add_css_class_to_children(settings_categories_box,"settings_categories_box")

        appearance_settings_button.connect('clicked',self.appearance_display)
        users_settings_button.connect('clicked',self.users_display)
        db_settings_button.connect('clicked',self.db_settings_display)
    def appearance_display(self,caller_obj):
        self.reload()
        label=Gtk.Label.new("Appearance settings")
        label.set_valign(Gtk.Align.START)
        self.settings_box.append(label)
        self.props.title="settings/appearance_settings"

    def users_display(self,caller_obj):
        self.reload()
        self.props.title="settings/users"
        if len(self.props.application.users.items()) == 0:
            message=Gtk.Label.new("No users in record!")
            message.set_valign(Gtk.Align.START)
            self.settings_box.append(message)
        for user_name,password in self.props.application.users.items():
            print("start")
            button=Gtk.CheckButton.new_with_label(user_name)
            self.settings_box.append(button)
            button.connect('activate',self.on_button_clicked,user_name)
            print("done")
    def on_button_clicked(self,caller_obj,parameter):
        self.props.application.current_user.set_state(GLib.Variant.new_string(paramater))

    def db_settings_display(self,caller_obj):
        self.reload()
        self.props.title="settings/database_directory"
        #database directory message display
        db_dir_box=Gtk.Box.new(Gtk.Orientation.HORIZONTAL,10)
        db_dir_box.set_valign(Gtk.Align.START)
        self.settings_box.append(db_dir_box)
        db_dir_label=Gtk.Label.new("Current database directory:")
        database_directory_entry_buffer=Gtk.EntryBuffer.new(self.props.application.current_db,-1)
        database_directory_textbox=Gtk.Entry.new_with_buffer(database_directory_entry_buffer)
        database_directory_textbox.set_overwrite_mode(False)
        database_directory_textbox.set_max_length(database_directory_textbox.get_text_length())
        #edit
        db_dir_edit_button=Gtk.Button.new_with_label("Edit")

        db_dir_box.append(db_dir_label)
        db_dir_box.append(database_directory_textbox)
        db_dir_box.append(db_dir_edit_button)

        db_dir_edit_button.connect('clicked',self.on_db_dir_edit_button_click,database_directory_textbox,database_directory_entry_buffer,db_dir_box)
    def on_db_dir_edit_button_click(self,caller_obj,db_entry,db_entry_buffer,db_dir_box):
        #change mode allow editing
        db_entry.set_overwrite_mode(True)
        db_entry.set_max_length(0)

        db_entry_contents=db_entry_buffer.get_text()
        #save the changes
        save_button=Gtk.Button.new_with_label("Save")
        db_dir_box.append(save_button)
        
        save_button.connect('clicked',self.db_dir_save_button_click,db_entry_contents,db_dir_box,db_entry)
    def db_dir_save_button_click(self,caller_obj,db_entry_contents,db_dir_box,db_entry):
        self.props.application.current_db=db_entry_contents
        print("saved")

        db_dir_box.remove(caller_obj)

        db_entry.set_overwrite_mode(True)
        db_entry.set_max_length(0)

    def reload(self):
        self.__init__()

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
        settings_button=Gtk.Button.new_with_label("Settings")
        #main menu buttons box
        main_menu_buttons_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        main_menu_buttons_box.set_valign(Gtk.Align.CENTER)
        main_menu_buttons_box.set_halign(Gtk.Align.CENTER)
        #buttons in box
        main_menu_buttons_box.append(reactions_button)
        main_menu_buttons_box.append(quiz_button)
        main_menu_buttons_box.append(simulator_button)
        main_menu_buttons_box.append(settings_button)
        main_menu_buttons_box.append(quit_button)
        self.set_child(main_menu_buttons_box)

        #css
        main_menu_buttons_box.add_css_class("main_menu_buttons_box")
        add_css_class_to_children(main_menu_buttons_box,"main_menu_buttons_box")

        #button functions
        reactions_button.set_action_name('app.open_reactions_page')
        quiz_button.connect('clicked',self.props.application.open_page,quiz_main_page)
        quit_button.set_action_name('app.quit')
        simulator_button.connect('clicked',self.props.application.open_page,simulator_page)
        settings_button.connect('clicked',self.props.application.open_page,settings_page)

#login page
class login_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="user login page")
        header_bar.set_titlebar(header_bar,self,settings=False)

        main_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,self.props.application.monitor_height/3)
        self.set_child(main_box)

        #page contents
        login_message=Gtk.Label.new()    
        entries_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        main_box.append(login_message)
        main_box.append(entries_box)

        #set behaviour
        entries_box.set_valign(Gtk.Align.CENTER)
        entries_box.set_halign(Gtk.Align.CENTER)
    
        login_message.set_markup(f'''
        <span font-size="{int(self.props.application.monitor_width/50)}pt">Login Form</span>''')

        #username and password
        user_name_storage=Gtk.EntryBuffer.new(None,-1)
        password_storage=Gtk.EntryBuffer.new(None,-1)
        
        user_name_entry=Gtk.Entry.new_with_buffer(user_name_storage)
        password_entry=Gtk.Entry.new_with_buffer(password_storage)

        user_name_entry.set_placeholder_text("user name")
        password_entry.set_placeholder_text("password")

        login_button=Gtk.Button.new_with_label("Login/Add")

        entries_box.append(user_name_entry)
        entries_box.append(password_entry)
        entries_box.append(login_button)

        #button functions
        login_button.connect('clicked',self.on_login_button_clicked,user_name_storage,password_storage)

    def on_login_button_clicked(self,caller_obj,user_name,password):
        #add user to users dict attribute in application class
        user_name=user_name.get_text()
        password=password.get_text()
        self.props.application.users[user_name]=password
        print(self.props.application.users,"user added, exiting")
        #open the last opened window
        self.props.application.open_page(None,self.props.application.window_history[-2])

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
        reactants_column=Gtk.ColumnViewColumn.new("reactants",reactants_column_signal_tracker)

        products_column_signal_tracker=Gtk.SignalListItemFactory.new()
        products_column=Gtk.ColumnViewColumn.new("products",products_column_signal_tracker)

        extra_info_column_signal_tracker=Gtk.SignalListItemFactory.new()
        extra_info_column=Gtk.ColumnViewColumn.new("extra_info",extra_info_column_signal_tracker)

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
