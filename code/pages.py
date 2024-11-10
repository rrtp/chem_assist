import gi,mysql.connector
gi.require_version("Gtk","4.0")
from gi.repository import Gtk,Gio,GObject,GLib

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

#header bar        
class header_bar(Gtk.HeaderBar):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    def set_titlebar(self,page,settings=True,back_button=True):
        page.set_titlebar(self())

        if settings==True:
            #settings button
            self.settings_button=Gtk.Button.new()
            settings_button_image=Gtk.Image.new_from_file(page.props.application.image_paths["settings"])
            self.settings_button.set_child(settings_button_image)
            #add to headerbar
            page.props.titlebar.pack_end(page.props.titlebar.settings_button)
            page.props.titlebar.settings_button.connect('clicked',page.props.application.open_page,settings_page)
            self.settings_button.add_css_class("iconbutton")
        if back_button==True:
            #back button
            self.back_button=Gtk.Button.new()
            back_button_image=Gtk.Image.new_from_file(page.props.application.image_paths["back"])
            self.back_button.set_child(back_button_image)
            #add to headerbar
            page.props.titlebar.back_button.connect('clicked',page.props.application.open_page,page.props.application.window_history[-2])
            page.props.titlebar.pack_start(page.props.titlebar.back_button)
            self.back_button.add_css_class("iconbutton")

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
    open_page=""

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="settings")
        header_bar.set_titlebar(header_bar,self,settings=False)

        self.main_box=Gtk.Box.new(Gtk.Orientation.HORIZONTAL,0)
        self.set_child(self.main_box)

        #scrolling support for window
        side_panel_scroll=Gtk.ScrolledWindow.new()
        self.settings_page_scroll=Gtk.ScrolledWindow.new()

        #do not shrink button width hen space is available
        side_panel_scroll.set_propagate_natural_width(True)
        self.settings_page_scroll.set_propagate_natural_width(True)

        settings_categories_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,0)
        side_panel_scroll.set_child(settings_categories_box)

        self.settings_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        self.settings_page_scroll.set_child(self.settings_box)

        self.main_box.append(side_panel_scroll)
        self.main_box.append(self.settings_page_scroll)

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

        #actions
        #users selection button
        user_button_activate_action=Gio.SimpleAction.new_stateful('current_user_button',GLib.VariantType.new("s"),GLib.Variant.new_string(self.props.application.current_user_action.props.state.get_string()))
        user_button_activate_action.connect('activate',self.on_activate_users_button)
        user_button_activate_action.connect('change_state',self.on_user_button_action_state_change)
        self.add_action(user_button_activate_action)

        #connection to db
        retry_connection_to_db_action=Gio.SimpleAction.new("retry_connection_to_db",None)
        retry_connection_to_db_action.connect('activate',self.retry_connection_to_db)
        self.add_action(retry_connection_to_db_action)

        #open users page window if open_page variable is set to users_page
        if self.open_page=="users_page":
            self.users_display(None)
            self.open_users_page=False

    #attempt to connect to database
    def retry_connection_to_db(self,caller_action,param):
        db_connection_return_value=self.props.application.connect_to_db(None,None)
        self.update_db_connection_button_refresh(None,db_connection_return_value)
    #on user button action state change
    def on_user_button_action_state_change(*args):
        print("state changed",args)
    #when user button is clicked
    def on_activate_users_button(self,caller_action,parameter):
        caller_action.set_state(parameter)
        self.props.application.current_user_action.set_state(caller_action.props.state)
        self.update_current_user_message(self.messages_box)
    #appearance settings page
    def appearance_display(self,caller_obj):
        self.reload()
        label=Gtk.Label.new("Appearance settings")
        label.set_valign(Gtk.Align.START)
        self.settings_box.append(label)
        self.props.title="settings/appearance"

    def users_display(self,caller_obj):
        self.reload()
        self.props.title="settings/users"

        users=self.props.application.users
        #no users message
        if len(self.props.application.users.items()) == 0:
            message=Gtk.Label.new("No users in record!")
            message.set_valign(Gtk.Align.START)
            self.settings_box.append(message)
        #users
        users_buttons_scroller=Gtk.ScrolledWindow.new()
        self.users_buttons_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,4)
        user_operations_box=Gtk.Box.new(Gtk.Orientation.HORIZONTAL,10)
        self.messages_box=Gtk.Box.new(Gtk.Orientation.HORIZONTAL,3)

        self.settings_box.append(users_buttons_scroller)
        self.settings_box.append(user_operations_box)
        self.settings_box.append(self.messages_box)

        users_buttons_scroller.set_propagate_natural_height(True)
        users_buttons_scroller.set_propagate_natural_width(True)
        users_buttons_scroller.set_child(self.users_buttons_box)

        self.update_users_buttons(users_buttons_scroller)

        #operations buttons
        add_user_button=Gtk.Button.new_with_label("Add user")
        remove_user_button=Gtk.Button.new_with_label("Remove current user")
        
        user_operations_box.append(remove_user_button)
        user_operations_box.append(add_user_button)
        
        add_user_button.connect('clicked',self.open_login_page)
        remove_user_button.connect('clicked',self.remove_current_user,users_buttons_scroller)

    def update_users_buttons(self,scroller):
        #replace current box
        self.users_buttons_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        scroller.set_child(self.users_buttons_box)

        button0=Gtk.CheckButton.new_with_label("No user")
        button0.set_action_name('win.current_user_button')
        button0.set_action_target_value(GLib.Variant.new_string(""))
        self.users_buttons_box.append(button0)
        for user_name in self.props.application.users.keys():
            button=Gtk.CheckButton.new_with_label(user_name)
            button.set_group(button0)
            button.set_action_name('win.current_user_button')
            button.set_action_target_value(GLib.Variant.new_string(user_name))
            self.users_buttons_box.append(button)
        self.update_current_user_message(self.messages_box)
    def remove_current_user(self,caller_obj,users_buttons_scroller):
        current_user=self.props.application.current_user_action.props.state.get_string()
        users=self.props.application.users
        if current_user=="":
            print("No current user")
            old_msg=self.messages_box.get_last_child()
            self.messages_box.remove(old_msg)
            self.messages_box.append(Gtk.Label.new("No current user!"))
            return
        if current_user not in users:
            print("ERROR:Current user not in users,user removed")
            return
        del self.props.application.users[current_user]
        self.props.application.update_users_file()
        #self.props.application.current_user=""
        self.props.application.current_user_action.set_state(GLib.Variant.new_string(""))
        self.update_users_buttons(users_buttons_scroller)
    def update_current_user_message(self,container):
        current_msg=container.get_last_child()
        if current_msg!=None:
            container.remove(current_msg)
        message=self.props.application.current_user_action.props.state.get_string()
        if message != "":
            message="current user: "+message
        label=Gtk.Label.new(message)
        self.messages_box.append(label)
    #add user
    def open_login_page(self,caller_obj):
        self.props.application.open_page(None,login_page)
    #set the state of current_user action to user_name of the given user
    def set_user(self,caller_obj,user_name):
        self.props.application.current_user_action.set_state(GLib.Variant.new_string(user_name))
        self.props.application.current_user=user_name
        self.update_current_user_message(self.messages_box)

    def db_settings_display(self,caller_obj):
        self.reload()
        self.props.title="settings/database"

        #database directory message display
        db_dir_box=Gtk.Box.new(Gtk.Orientation.HORIZONTAL,10)
        db_dir_box.set_valign(Gtk.Align.START)

        db_dir_label=Gtk.Label.new("Current database directory:")
        database_directory_entry_buffer=Gtk.EntryBuffer.new(self.props.application.db_name,-1)
        database_directory_textbox=Gtk.Entry.new_with_buffer(database_directory_entry_buffer)
        database_directory_textbox.set_overwrite_mode(False)
        database_directory_textbox.set_max_length(database_directory_textbox.get_text_length())
        
        db_dir_edit_button=Gtk.Button.new_with_label("Edit")
        db_dir_edit_button.connect('clicked',self.on_db_dir_edit_button_click,database_directory_textbox,database_directory_entry_buffer,db_dir_box)

        db_dir_box.append(db_dir_label)
        db_dir_box.append(database_directory_textbox)
        db_dir_box.append(db_dir_edit_button)

        #db connection status
        if self.props.application.db_cursor!=None:
            connection_status_message="Connection to database available"
        else:
            connection_status_message="Connection to database Unavailable!"

        db_connection_status_label=Gtk.Label.new(connection_status_message)
        connect_to_db_button=Gtk.Button.new_with_label("retry connecting to database")
        connect_to_db_button.set_action_name('win.retry_connection_to_db')

        #add to settings window
        self.settings_box.append(db_dir_box)
        self.settings_box.append(connect_to_db_button)
        self.settings_box.append(db_connection_status_label)
    #update the databse settings page message
    def update_db_connection_button_refresh(self,caller_obj,return_message=""):
        db_cursor=self.props.application.db_cursor
        db_cursor_status="cursor available"
        if db_cursor == None:
            db_cursor_status="No db cursor,error:\n"+str(return_message)
        message=Gtk.Label.new(db_cursor_status)
        self.settings_box.remove(self.settings_box.get_last_child())
        self.settings_box.append(message)
    def on_db_dir_edit_button_click(self,caller_obj,db_entry,db_entry_buffer,db_dir_box):
        #change mode allow editing
        db_entry.set_overwrite_mode(True)
        db_entry.set_max_length(0)
        db_dir_box.remove(caller_obj)
        db_entry_contents=db_entry_buffer.get_text()
        #save the changes
        save_button=Gtk.Button.new_with_label("Save")
        db_dir_box.append(save_button)
        
        save_button.connect('clicked',self.db_dir_save_button_click,db_entry_contents,db_dir_box,db_entry,caller_obj)
    #save the new database name
    def db_dir_save_button_click(self,caller_obj,db_entry_contents,db_dir_box,db_entry,edit_button):
        self.props.application.db_name=db_entry_contents
        print("saved")
        db_dir_box.remove(caller_obj)
        db_dir_box.append(edit_button)
        db_entry.set_overwrite_mode(True)
        db_entry.set_max_length(0)

    def reload(self):
        #relead the settings window by removing and adding new one
        self.settings_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        self.settings_page_scroll.set_child(self.settings_box)
        self.main_box.remove(self.main_box.get_last_child())
        self.main_box.append(self.settings_page_scroll)

#main menu page
class main_menu_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Chemistry assistant main page")
        self.props.name="main_menu_page"
        self.add_css_class("main_manu_page")

        main_menu_page_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,0)
        self.set_child(main_menu_page_box)

        #message box
        message_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,0)
        message_box_scroller=Gtk.ScrolledWindow()
        message_box_scroller.set_child(message_box)
        #main menu buttons box
        main_menu_buttons_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        main_menu_buttons_box.set_valign(Gtk.Align.CENTER)
        main_menu_buttons_box.set_halign(Gtk.Align.CENTER)
        #scroll for main menu buttons box
        main_menu_buttons_box_scroller=Gtk.ScrolledWindow()
        main_menu_buttons_box_scroller.set_child(main_menu_buttons_box)
        main_menu_buttons_box_scroller.set_propagate_natural_height(True)

        main_menu_page_box.append(message_box_scroller)
        main_menu_page_box.append(main_menu_buttons_box_scroller)

        #message label
        self.main_menu_message_box_label=Gtk.Label.new()
        message_box.append(self.main_menu_message_box_label)

        #buttons
        reactions_button=Gtk.Button.new_with_label("Reactions")
        quiz_button=Gtk.Button.new_with_label("Quiz")
        quit_button=Gtk.Button.new_with_label("Quit")
        simulator_button=Gtk.Button.new_with_label("Simulate")
        settings_button=Gtk.Button.new_with_label("Settings")

        #add buttons to box
        main_menu_buttons_box.append(reactions_button)
        main_menu_buttons_box.append(quiz_button)
        #main_menu_buttons_box.append(simulator_button)
        main_menu_buttons_box.append(settings_button)
        main_menu_buttons_box.append(quit_button)

        #css
        main_menu_buttons_box.add_css_class("main_menu_buttons_box")
        add_css_class_to_children(main_menu_buttons_box,"main_menu_buttons_box")

        #button functions
        reactions_button.set_action_name('app.open_reactions_page')
        quiz_button.set_action_name('app.open_quiz_page')
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

        #spinning animation box
        spnning_animation_box=Gtk.Box.new(Gtk.Orientation.HORIZONTAL,5)
        self.spinning_animation_message=Gtk.Label.new("Adding user..")
        self.spinning_animation_message.set_visible(False)
        self.spinning_animation=Gtk.Spinner.new()
        spnning_animation_box.append(self.spinning_animation_message)
        spnning_animation_box.append(self.spinning_animation)
        main_box.append(spnning_animation_box)
        main_box.set_halign(Gtk.Align.CENTER)
        #button functions
        login_button.connect('clicked',self.on_login_button_clicked,user_name_storage,password_storage)

    def on_login_button_clicked(self,caller_obj,user_name,password):
        #add user to users dict attribute in application class
        user_name=user_name.get_text()
        password=password.get_text()

        self.spinning_animation.start()
        self.spinning_animation_message.set_text("getting users")
        self.spinning_animation.set_visible(True)

        self.spinning_animation_message.set_text("adding user")
        #add the user
        self.props.application.users[user_name]=password
        self.props.application.current_user_action.set_state(GLib.Variant.new_string(user_name))
        self.props.application.current_user=user_name
        #stop spinning animation
        self.spinning_animation.stop()
        #print user added message
        print(self.props.application.users.keys(),"user added, exiting")
        #open the last opened window
        last_opened_window=self.props.application.window_history[-2]
        if last_opened_window == settings_page:
            last_opened_window.open_page="users_page"
        self.props.application.open_page(None,last_opened_window)

#quiz page
class quiz_main_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Quiz main page")
        header_bar.set_titlebar(header_bar,self)

        #main box
        quiz_main_page_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,0)
        self.set_child(quiz_main_page_box)

        #start quiz
        start_quiz_button=Gtk.Button.new_with_label("Start quiz")
        start_quiz_button.set_action_name('app.open_quiz')

        quiz_main_page_box.append(start_quiz_button)
class reaction_info(GObject.Object):
    def __init__(self,name,reactant,product,extra_info):
        super().__init__()
        self.name=name
        self.reactants=reactant
        self.products=product
        self.extra_info=extra_info

#Reactions page
class reactions_display_page(Gtk.ApplicationWindow):
    pull_data_from_reactions_table=False
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Reactions")
        ##db
        #connect to database server, create database and set it as current database
        connect_to_db_server_and_create_db_return=self.props.application.connect_to_db_server_and_create_db()
        #create reactions table
        create_reactions_table_return=False
        if connect_to_db_server_and_create_db_return==True:
            #creating the table
            create_reactions_table_return=self.props.application.create_reactions_table(self.props.application.db_cursor)
            #if reactions table connection exists, then only take data from there
            if create_reactions_table_return==True:
                self.pull_data_from_reactions_table=True
            else:
                #display error and exit function with return value as false
                if self.props.application.window_history[-1] == main_menu_page:
                    self.props.application.props.active_window.main_menu_message_box_label.set_text("Error: "+str(create_reactions_table_return))
                print("could not create reactions table")

        ##title
        title_message="Reactions"
        #user
        if self.props.application.current_user_action.props.state.get_string()!=None:
            title_message=title_message+" (user:"+self.props.application.current_user_action.props.state.get_string()+")"
        #database
        if self.props.application.db_cursor == None:
            title_message=title_message+"(no db connection)"
        elif self.props.application.database_object.is_connected():
            title_message=title_message[:-1]+",database:"+self.props.application.db_name+")"
        self.set_title(title_message)
        #titlebar
        header_bar.set_titlebar(header_bar,self)

        ##layout
        reactions_page_box_scroller=Gtk.ScrolledWindow.new()
        self.set_child(reactions_page_box_scroller)
        #boxes
        reactions_page_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        reactions_page_box.set_homogeneous(True)
        reactions_page_box_scroller.set_child(reactions_page_box)
        #self.set_child(reactions_page_box)

        reactions_list_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        reactions_page_bottom_panel_box=Gtk.Box.new(Gtk.Orientation.HORIZONTAL,10)

        reactions_page_box.append(reactions_list_box)
        if self.pull_data_from_reactions_table == True:
            reactions_page_box.append(reactions_page_bottom_panel_box)

        #box properties
        reactions_page_box.set_halign(Gtk.Align.FILL)
        reactions_page_bottom_panel_box.set_valign(Gtk.Align.END)
        reactions_page_bottom_panel_box.set_halign(Gtk.Align.CENTER)
        
        ##reactions list
        #list storage
        self.reactions_list=Gio.ListStore.new(reaction_info)
        self.reactions_list_multiselection=Gtk.MultiSelection.new(self.reactions_list)

        #fetch data from database and add it to reactions list
        if self.pull_data_from_reactions_table==True:
            self.add_reactions_data_to_list()
        #if there is not database connection, display message
        if self.pull_data_from_reactions_table==False:
            no_connection_message=Gtk.Label.new("No database connection!")
            Gtk.Box.insert_child_after(reactions_page_box,no_connection_message,reactions_page_box.get_first_child())

        #name column
        name_column_signal_factory=Gtk.SignalListItemFactory.new()
        name_column=Gtk.ColumnViewColumn.new("name",name_column_signal_factory)
        #reactants column
        reactants_column_signal_factory=Gtk.SignalListItemFactory.new()
        reactants_column=Gtk.ColumnViewColumn.new("reactants",reactants_column_signal_factory)
        #products column
        products_column_signal_factory=Gtk.SignalListItemFactory.new()
        products_column=Gtk.ColumnViewColumn.new("products",products_column_signal_factory)
        #extra info column
        extra_info_column_signal_factory=Gtk.SignalListItemFactory.new()
        extra_info_column=Gtk.ColumnViewColumn.new("extra_info",extra_info_column_signal_factory)
        extra_info_column.props.resizable=True

        #display items
        name_column_signal_factory.connect("setup",self.add_label_to_column)
        reactants_column_signal_factory.connect("setup",self.add_label_to_column)
        products_column_signal_factory.connect("setup",self.add_label_to_column)
        extra_info_column_signal_factory.connect("setup",self.add_label_to_column)

        name_column_signal_factory.connect("bind",self.set_column_cell_label,1)
        reactants_column_signal_factory.connect("bind",self.set_column_cell_label,2)
        products_column_signal_factory.connect("bind",self.set_column_cell_label,3)
        extra_info_column_signal_factory.connect("bind",self.set_column_cell_label,4)

        name_column_signal_factory.connect("unbind",self.remove_element_from_column)
        reactants_column_signal_factory.connect("unbind",self.remove_element_from_column)
        products_column_signal_factory.connect("unbind",self.remove_element_from_column)
        extra_info_column_signal_factory.connect("unbind",self.remove_element_from_column)

        #create column view
        self.reactions_column_manager=Gtk.ColumnView.new(self.reactions_list_multiselection)
        self.reactions_column_manager.append_column(name_column)
        self.reactions_column_manager.append_column(reactants_column)
        self.reactions_column_manager.append_column(products_column)
        self.reactions_column_manager.append_column(extra_info_column)

        #add to box
        reactions_list_box.append(self.reactions_column_manager)

        ##bottom panel
        refresh_button=Gtk.Button.new_with_label("Refresh")
        reactions_db_import_button=Gtk.Button.new_with_label("Import")
        reactions_db_export_button=Gtk.Button.new_with_label("Export")
        reactions_db_add_button=Gtk.Button.new_with_label("Add")

        #button properties
        refresh_button_image=Gtk.Image.new_from_file(self.props.application.image_paths["refresh"])
        refresh_button.set_child(refresh_button_image)
        #add button to bottom panel
        reactions_page_bottom_panel_box.append(refresh_button)
        reactions_page_bottom_panel_box.append(reactions_db_import_button)
        reactions_page_bottom_panel_box.append(reactions_db_export_button)
        reactions_page_bottom_panel_box.append(reactions_db_add_button)   
        #button functions
        refresh_button.connect('activate',self.refresh_reactions_list)
        reactions_db_add_button.connect('clicked',self.add_reaction_to_db)
    def refresh_reactions_list(self,caller_obj):
        reactions_list=self.reactions_list_multiselection.get_model()
        #clear list
        reactions_list.remove_all()
        #add data to list
        self.add_reactions_data_to_list()

        columns=self.reactions_column_manager.get_columns()
        for column_number in range(columns.get_n_items()):
            columns[column_number].get_factory().emit("unbind")
        for column_number in range(columns.get_n_items()):
            columns[column_number].get_factory().emit("bind")
        print("[reactions display page]refreshed columns")
    def add_label_to_column(self,caller_factory,column_cell):
        column_cell.set_child(Gtk.Label.new())
    def set_column_cell_label(self,caller_factory,column_cell,column_number):
        #cell label
        label=column_cell.get_child()
        #cell position
        cell_position=column_cell.get_position()
        #reactions list
        reactions_list=self.reactions_list_multiselection.get_model()
        #reaction object
        reaction_details=reactions_list[cell_position]
        column_num_to_column_val_dict={
            1:reaction_details.name,
            2:reaction_details.reactants,
            3:reaction_details.products,
            4:reaction_details.extra_info
        }
        label_text=column_num_to_column_val_dict[column_number]
        #set entry value
        column_cell.get_child().set_text(label_text)
    def remove_element_from_column(self,caller_factory,column_cell):
        column_cell.get_child().set_text("")

    #add reaction to reactions table
    def add_reaction_to_db(self,caller_obj):
        self.props.application.open_page(None,add_reaction_to_db_page)
    
    #get reactions from reactions table and add them to list
    def add_reactions_data_to_list(self):
        get_data_from_reactions_table_command="select * from reactions"
        #get reactions data from database
        self.props.application.db_cursor.execute(get_data_from_reactions_table_command)
        reactions_list=self.props.application.db_cursor.fetchall()
        #reaction list to gobject, append to list
        for reaction in reactions_list:
            reaction_gobject=reaction_info(reaction[1],reaction[2],reaction[3],reaction[4])
            self.reactions_list.append(reaction_gobject)
            # for i in range(self.reactions_list.get_n_items()):
            #     print(self.reactions_list.get_item(i).name)

#add reactions to table page
class add_reaction_to_db_page(Gtk.ApplicationWindow):
    def __init__(self,reaction_information=["","","",""],*args,**kwargs):
        super().__init__(*args,**kwargs,title="Add reaction to database")
        header_bar.set_titlebar(header_bar,self)

        main_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,10)
        self.set_child(main_box)

        reactant_entry_buffer=Gtk.EntryBuffer.new(reaction_information[0],-1)
        name_entry_buffer=Gtk.EntryBuffer.new(reaction_information[1],-1)
        product_entry_buffer=Gtk.EntryBuffer.new(reaction_information[2],-1)
        extra_info_entry_buffer=Gtk.EntryBuffer.new(reaction_information[3],-1)
        
        reactant_entry=Gtk.Entry.new_with_buffer(reactant_entry_buffer)
        name_entry=Gtk.Entry.new_with_buffer(name_entry_buffer)
        product_entry=Gtk.Entry.new_with_buffer(product_entry_buffer)
        extra_info_entry=Gtk.Entry.new_with_buffer(extra_info_entry_buffer)

        reactant_entry.set_placeholder_text("reactants")
        name_entry.set_placeholder_text("name")
        product_entry.set_placeholder_text("products")
        extra_info_entry.set_placeholder_text("extra info")

        add_button=Gtk.Button.new_with_label("Add reaction to database")
        add_button.set_halign(Gtk.Align.CENTER)
        main_box.append(reactant_entry)
        main_box.append(name_entry)
        main_box.append(product_entry)
        main_box.append(extra_info_entry)
        main_box.append(add_button)
        
        #reaction_details_buffers=(reactant_entry_buffer,name_entry_buffer,product_entry_buffer,extra_info_entry_buffer)
        add_button.connect('clicked',self.add_reaction_to_db,(reactant_entry_buffer,name_entry_buffer,product_entry_buffer,extra_info_entry_buffer))
    def add_reaction_to_db(self,caller_obj,reaction_details_buffers):
        #columns
        columns=self.props.application.reactions_table_columns
        columns_str=""
        for i in columns:
            columns_str = columns_str + i + ","
        columns_str=columns_str[:-1]
        #values
        values_str=""
        for i in reaction_details_buffers:
            i=i.get_text()
            values_str=values_str+"'"+i+"',"
        values_str=values_str[:-1]
        #insert details in table
        try:
            insert_reaction_string=f"insert into reactions ({columns_str}) values({values_str});"
            self.props.application.db_cursor.execute(insert_reaction_string)
            self.props.application.database_object.commit()
        except mysql.connector.Error as err:
            print("Error while inserting reactions details into table:\n",err)
        #open previous window
        previous_window=self.props.application.window_history[-2]
        self.props.application.open_page(None,previous_window)
class simulator_page(Gtk.ApplicationWindow):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs,title="Simulator")
        header_bar.set_titlebar(header_bar,self)
        reaction_box=Gtk.Box.new(Gtk.Orientation.VERTICAL,0)