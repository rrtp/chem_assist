import gi

gi.require_version("Adw", "1")
gi.require_version("Gtk", "4.0")

from gi.repository import Adw, Gio, GObject, Gtk, Gdk


class Person(GObject.Object):
    __gtype_name__ = "Person"

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
        super().__init__(application=app, title="REACTIONS PAGE", default_width=400, default_height=400)

        self.model = Gio.ListStore(item_type=Person)

        # Initial entries
        for _ in range(5):  
            self.model.append(Person())

        # Create UI elements
        self.cv = Gtk.ColumnView(model=Gtk.NoSelection(model=self.model))
        self._create_column_view()

        # Create a smaller button to add new entries
        add_button = Gtk.Button(label="Add Columns")
        add_button.set_size_request(80, 30)  # Set button size
        add_button.connect("clicked", self.on_add_entry)

        # Set margins for the button
        add_button.set_margin_start(5)
        add_button.set_margin_bottom(5)

        # Adjust the Layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        main_box.props.margin_start = 12
        main_box.props.margin_end = 12
        main_box.props.margin_top = 12
        main_box.props.margin_bottom = 12

        title_label = Gtk.Label(label="REACTIONS")
        title_label.set_halign(Gtk.Align.START)
        main_box.append(title_label)

        # Create a scrolled window to contain the column view
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_vexpand(True)
        scrolled_window.set_child(self.cv)

        main_box.append(scrolled_window)

        # Create a box for the button to position it at the bottom left
        button_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        button_box.append(add_button)

        # Add button box to the main box
        main_box.append(button_box)

        self.set_child(main_box)

    def _create_column_view(self):
        # Factory for serial number
        factory1 = Gtk.SignalListItemFactory()
        factory1.connect("setup", self._on_factory_setup_text_entry)
        factory1.connect("bind", self._on_factory_bind, "serial_no")

        # Factory for name
        factory2 = Gtk.SignalListItemFactory()
        factory2.connect("setup", self._on_factory_setup_text_entry)
        factory2.connect("bind", self._on_factory_bind, "name")

        # Factory for reactions
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
        new_person = Person()
        new_person.serial_no = str(self.model.get_n_items() + 1)  # Auto-increment serial number
        self.model.append(new_person)

    def _on_factory_setup_text_entry(self, factory, list_item):
        entry = Gtk.Entry()
        list_item.set_child(entry)

    def _on_factory_bind(self, factory, list_item, property_name):
        child = list_item.get_child()
        person = list_item.get_item()
        child.bind_property("text", person, property_name, GObject.BindingFlags.SYNC_CREATE)

    def _on_factory_teardown(self, factory, list_item):
        pass


class ExampleApp(Adw.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        window = ExampleWindow(self)
        window.present()


app = ExampleApp()
app.run()
