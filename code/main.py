import gi,os,mysql.connector
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk,Gio,GLib
from mysql.connector import errorcode
import pages
import quiz

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

#custom gtk application class containing helpful definitions
class Application(Gtk.Application):
    #window history
    window_history_limit=10
    window_history=[]

    #default display
    default_display=Gdk.Display.get_default()

    #css file
    css_file_path=css_dir+"styles.css"
    css_provider=Gtk.CssProvider.new()

    #database file path
    db_name="chem_assist_db1"
    db_cursor=None
    database_object=None

    #config file
    users_file_path="users.conf"
    #users
    current_user=""
    users={"chem_assist_user":"chem_assist_user_password"}

    #images
    settings_image_path=image_paths["settings"]
    back_image_path=image_paths["back"]
    app_image_path=image_paths["app"]

    reactions_table_columns=("name","reactant","product","extra_info")
    #constructor
    def __init__(self):
        super().__init__(application_id="com.chem_assist_project.chem_assist")
        self.connect('activate',self.on_activate)

    #on activate app
    def on_activate(self,app):
        print("activated")
        #get monitor dimentions
        self.primary_monitor=self.default_display.get_monitors()[0]
        self.get_monitor_dimentions(self.primary_monitor)
        #load css file
        self.css_provider.load_from_path(self.css_file_path)
        self.add_styles_from_provider(self.css_provider)

        #define actions
        quit_action=Gio.SimpleAction.new("quit",None)
        quit_action.connect('activate',self.close_page)
        self.add_action(quit_action)
        

        open_reactions_page_action=Gio.SimpleAction.new("open_reactions_page",None)
        open_reactions_page_action.connect('activate',self.on_open_reactions_page)
        self.add_action(open_reactions_page_action)

        self.current_user_action=Gio.SimpleAction.new_stateful("current_user",GLib.VariantType.new("s"),GLib.Variant.new_string("chem_assist_user"))
        self.add_action(self.current_user_action)

        open_quiz_action=Gio.SimpleAction.new("open_quiz",None)
        open_quiz_action.connect('activate',self.open_quiz_page)
        self.add_action(open_quiz_action)

        self.connect_to_db_action=Gio.SimpleAction.new("connect_to_db",None)
        self.connect_to_db_action.connect('activate',self.connect_to_db)
        self.add_action(self.connect_to_db_action)

        #open welcome page
        self.open_page(None,pages.welcome_page)
    #connect to db
    def connect_to_db(self,caller_action,parameter):
        #connect to server
        return_value_from_connect=self.connect_to_db_server()
        #do not contiunue if no cursor is available
        if return_value_from_connect != True:
            return return_value_from_connect
        #get cursor
        return_value_from_get_cursor=self.get_cursor_from_db_connection(self.database_object)
        #return the error if failed to get cursor
        if return_value_from_get_cursor !=True:
            return return_value_from_get_cursor
        return True
    #reactions page open
    def on_open_reactions_page(self,caller_obj,arg3):
        #connect to db server and get cursor
        connect_to_db_return=self.connect_to_db(None,None)
        if connect_to_db_return != True:
            #display error and exit function
            print("[Error:database connection],not connecting to reactions table")
            if self.window_history[-1] == pages.main_menu_page:
                self.props.active_window.main_menu_message_box_label.set_text("Error: "+str(connect_to_db_return))
            return False
        #create database
        create_db_return=self.create_db(self.db_cursor)
        if create_db_return != True:
            #display error in main_menu page message box and exit the function
            if self.window_history[-1] == pages.main_menu_page:
                self.props.active_window.main_menu_message_box_label.set_text("Error: "+str(create_db_return))
            return False
        #create reactions table
        create_reactions_table_return=self.create_reactions_table(self.db_cursor)
        if create_reactions_table_return != True:
            #display error and exit function with return value as false
            if self.window_history[-1] == pages.main_menu_page:
                self.props.active_window.main_menu_message_box_label.set_text("Error: "+str(create_reactions_table_return))
            return False
        #open reactions page
        self.open_page(None,pages.reactions_display_page)

    #Open quiz page
    def open_quiz_page(self,*args):
        #database setup
        self.connect_to_db("None","None")
        self.create_db(self.db_cursor)

        #open quiz.py quiz window
        quiz.main(self.database_object)

    #get monitor dimentions
    def get_monitor_dimentions(self,monitor):
        monitor_geometry=monitor.get_geometry()
        self.monitor_width=monitor_geometry.width
        self.monitor_height=monitor_geometry.height
    #load styles to context
    def add_styles_from_provider(self,css_provider):
        Gtk.StyleContext.add_provider_for_display(self.default_display,css_provider,Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    #close current page
    def close_page(self,caller_obj=None,page=None):
        if page!=None:
            page.close()
        if page==None and self.get_active_window()!=None:
            self.props.active_window.close()
    #open page
    def open_page(app,caller_obj,page):
        app.close_page(page=app.props.active_window)

        app.window_history.append(page)
        app.window_history_size=len(app.window_history)
        #solve back button window loop problem
        if app.window_history_size > 3 and app.window_history[-1] == app.window_history[-3]:
            app.window_history.pop()
            app.window_history.pop()
        #trim window history if greater than limit
        if app.window_history_size>app.window_history_limit:
            del app.window_history[0]

        page=page(application=app)
        page.set_default_size(app.monitor_width/2,app.monitor_height/2)
        page.present()

    #database operations
    def connect_to_db_server(self):
        #please take backup of database before connecting with path as it may be deleted by this function
        connection_profile={
            "user":self.current_user_action.props.state.get_string(),
            "password":self.users[self.current_user_action.props.state.get_string()],
            }
        try:
            self.database_object=mysql.connector.connect( **connection_profile)
        except mysql.connector.Error as err:
            message="Error while connecting to database: "+str(err)
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                message=f"Access denied for user {self.current_user_action.props.state.get_string()}"
            print(message)
            return err
        return True
    def get_cursor_from_db_connection(self,db_connection_object):
        if db_connection_object == None:
            print(f"cannot get cursor, no database connection obj")
            return
        try:
            self.db_cursor=db_connection_object.cursor()
        except mysql.connector.Error as err:
            print(f"Error while getting cursor from database connection: {err}: Database_connection:{self.database_object.is_connected}")
            return err
        print("=>cursor connected")
        return True

    def create_db(self,db_cursor):
        #create database
        try:
            db_cursor.execute(f'create database {self.db_name};')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_DB_CREATE_EXISTS:
                #if database already exists
                msg_str=f"=>database {self.db_name} found"
                print(msg_str)
            else:
                print("Error while CREATING database",err)
                return err
        #use database
        try:
            db_cursor.execute(f'use {self.db_name};')
        except mysql.connector.Error as err:
            print("Error while USING database",err)
            return err
        print(f'=>using database {self.db_name}')
        return True
    def create_reactions_table(self,db_cursor):
        try:
            create_reactions_table_sql_command='''CREATE TABLE reactions(
                reaction_entry_number int auto_increment primary key,
                name varchar(255),
                reactant varchar(255),
                product varchar(255),
                extra_info varchar(255));'''
            db_cursor.execute(create_reactions_table_sql_command)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("=>reactions table found")
                return True
            else:
                print("eror while creating table \"reactions\"", err)
                return err

#Create an instance of Application
app=Application()
app.run(None)