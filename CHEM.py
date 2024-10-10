import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Chemistry Assist")
        self.set_default_size(800, 600)

        # Set the window name for CSS styling
        self.set_name("main_window")

        # Load the CSS for background
        self.load_css()

        # Create the main button
        self.button = Gtk.Button(label="LETS START!!!")
        self.button.connect("clicked", self.on_button_clicked)

        # Add button to the window
        self.add(self.button)

    def load_css(self):
        # CSS style for the background image of the main window
        css = b"""
        #main_window {
            background-image: url("Documents/chemB.png");  /* Ensure this path is correct */
            background-size: cover;
            background-repeat: no-repeat;
        }
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)

        # Apply CSS to the window
        self.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def on_button_clicked(self, widget):
        # Open a new window
        new_window = NewWindow()
        new_window.show_all()

class NewWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="ACTIVITIES")
        self.set_default_size(800, 600)

        # Set the window name for CSS styling
        self.set_name("new_window")

        # Load the CSS for background
        self.load_css()

        # Create a vertical box to center the buttons
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_halign(Gtk.Align.CENTER)
        vbox.set_valign(Gtk.Align.CENTER)

        # Create two buttons
        button1 = Gtk.Button(label="REACTIONS")
        button2 = Gtk.Button(label="EXTRAS")

        # Connect button signals to their respective methods
        button1.connect("clicked", self.on_button1_clicked)
        button2.connect("clicked", self.on_button2_clicked)

        # Add buttons to the box
        vbox.pack_start(button1, True, True, 0)
        vbox.pack_start(button2, True, True, 0)

        # Add the box to the window
        self.add(vbox)

    def load_css(self):
        # CSS style for the background image of the new window
        css = b"""
        #new_window {
            background-image: url("Documents/chemB.png");  /* Ensure this path is correct */
            background-size: cover;
            background-repeat: no-repeat;
        }
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)

        # Apply CSS to the window
        self.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def on_button1_clicked(self, widget):
        # Open a new window with a specific background image
        window1 = CustomWindow("Pictures/green.png")  # Specify the desired background
        window1.show_all()

    def on_button2_clicked(self, widget):
        # Open a new window with a different specific background image
        window2 = CustomWindow("Pictures/green.png")  # Specify another desired background
        window2.show_all()

class CustomWindow(Gtk.Window):
    def __init__(self, background_image):
        super().__init__(title="REACTIONS")
        self.set_default_size(800, 600)

        # Load the CSS for background
        self.load_css(background_image)

        # Create a button to go back
        back_button = Gtk.Button(label="←")  # Arrow symbol for back
        back_button.set_size_request(30, 30)  # Small size of the button
        back_button.connect("clicked", self.on_back_button_clicked)

        # Create a settings button
        settings_button = Gtk.Button(label="⚙️")  # Gear icon for settings
        settings_button.set_size_request(30, 30)  # Small size of the button
        settings_button.connect("clicked", self.on_settings_button_clicked)

        # Create a header bar for the buttons
        header_bar = Gtk.HeaderBar()
        header_bar.pack_start(back_button)
        header_bar.pack_end(settings_button)  # Add settings button to the right
        self.set_titlebar(header_bar)

        # Set the background image as the main area
        self.set_name("custom_window")

    def load_css(self, background_image):
        # CSS style for the background image of the custom window
        css = f"""
        #custom_window {{
            background-image: url("{background_image}");
            background-size: cover;
            background-repeat: no-repeat;
        }}
        """.encode('utf-8')

        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)

        # Apply CSS to the window
        self.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

    def on_back_button_clicked(self, widget):
        # Close the current window
        self.destroy()

    def on_settings_button_clicked(self, widget):
        # Open settings window
        settings_window = SettingsWindow()
        settings_window.show_all()

class SettingsWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Settings")
        self.set_default_size(400, 300)

        # Load the CSS for background
        self.load_css()

        # Create a label for the settings window
        label = Gtk.Label(label="ANY HELP!")
        self.add(label)

    def load_css(self):
        # CSS style for the background image of the settings window
        css = b"""
        #settings_window {
            background-color: #e0e0e0;  /* Light gray background for settings */
            background-size: cover;
        }
        """
        style_provider = Gtk.CssProvider()
        style_provider.load_from_data(css)

        # Apply CSS to the window
        self.get_style_context().add_provider(style_provider, Gtk.STYLE_PROVIDER_PRIORITY_USER)

def main():
    window = MainWindow()
    window.connect("destroy", Gtk.main_quit)  # Ensure the application can quit
    window.show_all()
    Gtk.main()  # Start the main loop

if __name__ == "__main__":
    main()
