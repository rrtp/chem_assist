import gi
import sqlite3

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GObject

class reactions(GObject.Object):
    __gtype_name__ = "Reactions"

    def __init__(self):
        super().__init__()
        self._serial_no = ""
        self._name = ""
        self._reactions = ""

    @GObject.Property(type=str)
    def serial_no(self):
        return self._serial_no

    @GObject.Property(type=str)
    def name(self):
        return self._name

    @GObject.Property(type=str)
    def reactions(self):
        return self._reactions

class ExampleWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Reactions Page", default_width=400, default_height=400)

        self.model = Gio.ListStore(item_type=reactions)

        # Create DB connection and table
        self.conn = sqlite3.connect('DATABASE.db')
        self._create_table()

        # Load existing people from the database
        self.load_reactions()

        # Create UI elements
        self.cv = Gtk.ColumnView(model=Gtk.NoSelection(model=self.model))
        self._create_column_view()

        add_button = Gtk.Button(label="Add Columns")
        add_button.set_size_request(80, 30)
        add_button.connect("clicked", self.on_add_entry)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        main_box.set_margin_start(12)
        main_box.set_margin_end(12)
        main_box.set_margin_top(12)
        main_box.set_margin_bottom(12)

        title_label = Gtk.Label(label="Reactions")
        title_label.set_halign(Gtk.Align.START)
        main_box.append(title_label)

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.set_child(self.cv)

        main_box.append(scrolled_window)

        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        button_box.append(add_button)

        main_box.append(button_box)

        self.set_child(main_box)

    def _create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS people (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                serial_no TEXT,
                name TEXT,
                reactions TEXT
            )
        ''')
        self.conn.commit()

    def load_reactions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT serial_no, name, reactions FROM people")
        for serial_no, name, reactions in cursor.fetchall():
            reactions = Person()
            reactions.serial_no = serial_no
            reactions.name = name
            reactions.reactions = reactions
            self.model.append(reactions)

    def _create_column_view(self):
        factory1 = Gtk.SignalListItemFactory()
        factory1.connect("setup", self._on_factory_setup_text_entry)
        factory1.connect("bind", self._on_factory_bind, "serial_no")

        factory2 = Gtk.SignalListItemFactory()
        factory2.connect("setup", self._on_factory_setup_text_entry)
        factory2.connect("bind", self._on_factory_bind, "name")

        factory3 = Gtk.SignalListItemFactory()
        factory3.connect("setup", self._on_factory_setup_text_entry)
        factory3.connect("bind", self._on_factory_bind, "reactions")

        col1 = Gtk.ColumnViewColumn(title="S.No", factory=factory1, resizable=True)
        col1.props.expand = True
        self.cv.append_column(col1)

        col2 = Gtk.ColumnViewColumn(title="Name", factory=factory2, resizable=True)
        col2.props.expand = True
        self.cv.append_column(col2)

        col3 = Gtk.ColumnViewColumn(title="Reactions", factory=factory3, resizable=True)
        col3.props.expand = True
        self.cv.append_column(col3)

        self.cv.props.hexpand = True
        self.cv.props.vexpand = True

    def on_add_entry(self, button):
        new_reactions = reactions()
        new_reactions.serial_no = str(self.model.get_n_items() + 1)  # Auto-increment serial number
        new_reactions.name = "New Name"  # You can set a default name
        new_reactions.reactions = "New Reaction"  # You can set a default reaction
        self.model.append(new_reactions)
        self.save_reactions_to_db(new_reactions)

    def save_reactions_to_db(self, reactions):
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO reactions (serial_no, name, reactions) VALUES (?, ?, ?)",
                       (reactions.serial_no, reactions.name, reactions.reactions))
        self.conn.commit()

    def _on_factory_setup_text_entry(self, factory, list_item):
        entry = Gtk.Entry()
        list_item.set_child(entry)

    def _on_factory_bind(self, factory, list_item, property_name):
        child = list_item.get_child()
        reactions = list_item.get_item()
        child.bind_property("text", reactions, property_name, GObject.BindingFlags.SYNC_CREATE)

class ExampleApp(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        window = ExampleWindow(self)
        window.present()

app = ExampleApp()
app.run()
