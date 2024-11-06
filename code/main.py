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
    current_db=db_dir+"test.db"

    #config file
    users_file_path="users.conf"
    #users
    current_user=""
    users={}

    #images
    settings_image_path=image_paths["settings"]
    back_image_path=image_paths["back"]
    app_image_path=image_paths["app"]

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

        self.current_user_action=Gio.SimpleAction.new_stateful("current_user",GLib.VariantType.new("s"),GLib.Variant.new_string(""))
        self.add_action(self.current_user_action)

        open_quiz_action=Gio.SimpleAction.new("open_quiz",None)
        open_quiz_action.connect('activate',self.open_quiz_page)
        self.add_action(open_quiz_action)

        #open welcome page
        self.open_page(None,pages.welcome_page)
    #reactions page open
    def on_open_reactions_page(self,caller_obj,arg3):
            if self.current_user == None:
                self.setup_user()
                print("setting up")

            elif self.current_user!=None:
                self.open_page(None,pages.reactions_display_page)

    #Open quiz page
    def open_quiz_page(*args):
        pass

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
    def connect_to_db(self,db_path,populate=False):
        #please take backup of database before connecting with path as it may be deleted by this function
        connection_profile={
            "user":self.props.application.current_user_action.props.state.get_string(),

        }
        try:
            database_object=mysql.connector.connect(connection_profile)
        except mysql.connector.Error as err:
            print("error while connecting to database server:",err)
            return
        db_cursor=database_object.cursor()
        return db_cursor
    def populate_db(self,db_cursor):
        db_cursor.execute('CREATE TABLE questions(question varchar,option1 varchar,option2 varchar,option3 varchar,option4 varchar,answer varchar,extra_info varchar)')
        db_cursor.execute('CREATE TABLE reactions(name varchar,reactant varchat,product varchar,extra_info varchar)')
    def get_data_from_db(self,table_name,db_cursor):
        db_data=db_cursor.execute(f'SELECT * FROM {table_name}')
        return db_data

#Create an instance of Application
app=Application()
app.run(None)