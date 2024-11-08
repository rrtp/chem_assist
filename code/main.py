import gi,os,mysql.connector
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk,Gdk,Gio,GLib
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
    current_db_name="chem_assist_db1"
    db_cursor=None
    database_object=None

    #config file
    users_file_path="users.conf"
    #users
    current_user=""
    users={"chem_assist_user":"chem_assist_user_password","root":"Mysql@root"}

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

        self.current_user_action=Gio.SimpleAction.new_stateful("current_user",GLib.VariantType.new("s"),GLib.Variant.new_string("root"))
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
        self.connect_to_db_server()
        #if error return error
        if type(self.database_object) == mysql.connector.errors.ProgrammingError:
            return self.database_object
        self.db_cursor=self.get_cursor_from_db_connection(self.database_object)
    #make the database and tables
    def setup_database(self,db_cursor):
        self.create_db(db_cursor)
        self.populate_db(db_cursor)
    #reactions page open
    def on_open_reactions_page(self,caller_obj,arg3):
        self.connect_to_db(None,None)
        if type(self.db_cursor) == mysql.connector.errors.ProgrammingError or self.db_cursor==None:
            print("ERROR while obtaining connector to database",self.db_cursor)
            return
        self.setup_database(self.db_cursor)
        self.get_data_from_db("reactions",self.db_cursor)
        self.open_page(None,pages.reactions_display_page)

    #Open quiz page
    def open_quiz_page(self,*args):
        self.connect_to_db(None,None)
        self.db_cursor.execute(f"use {self.current_db_name}")
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
        if app.window_history_size > 3 and app.window_history[-1] == app.window_history[-3]:
            app.window_history.pop()
            app.window_history.pop()
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
            print("error while connecting to database server:",err)
            return err
    def get_cursor_from_db_connection(self,db_connection_object):
        try:
            db_cursor=db_connection_object.cursor()
        except mysql.connector.Error as err:
            print("Error while creating cursor",err)
            return err
        return db_cursor
    def create_db(self,db_cursor):
        #create database
        try:
            db_cursor.execute(f'create database {self.current_db_name};')
            print("CURSORRR: ",self.db_cursor, db_cursor)
        except mysql.connector.Error as err:
            print("Error while CREATING database",err)
        #use database
        try:
            db_cursor.execute(f'use {self.current_db_name};')
            print('using database')
        except mysql.connector.Error as err:
            print("Error while USING database",err)

    def populate_db(self,db_cursor):
        try:
            db_cursor.execute('CREATE TABLE questions(question varchar(255),option1 varchar(255),option2 varchar(255),option3 varchar(255),option4 varchar(255),answer varchar(255),extra_info varchar(255));')
        except mysql.connector.Error as err:
            print("eror while creating table \"questions\"", err)
        try:
            db_cursor.execute('CREATE TABLE reactions(name varchar(255),reactant varchar(255),product varchar(255),extra_info varchar(255));')
        except mysql.connector.Error as err:
            print("eror while creating table \"reactions\"", err)
    def get_data_from_db(self,table_name,db_cursor):
        db_data=db_cursor.execute(f'SELECT * FROM {table_name}')
        print(db_data)
        return db_data

#Create an instance of Application
app=Application()
app.run(None)