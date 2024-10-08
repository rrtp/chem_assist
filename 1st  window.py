import gi
import sys

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Adw, Gtk

class MyApplication(Adw.Application):
    """The main application."""

    def __init__(self):
        super().__init__(application_id="org.example.MyApp")
    
    def do_activate(self):
        # Create a Gtk.Window belonging to the application
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("Welcome to Chemistry Assist")
        
        window.set_resizable(True)
        

        # Create a Gtk.Overlay to hold the image and the label
        overlay = Gtk.Overlay()
        overlay.set_hexpand(True)
        overlay.set_vexpand(True)

        # Create a Gtk.Image for the background
        image = Gtk.Image.new_from_file("background.png")  # Replace with your image path
        image.set_size_request(0,0)
        image.set_hexpand(False)
        image.set_vexpand(False)
        image.set_halign(Gtk.Align.FILL)
        image.set_valign(Gtk.Align.FILL)

        # Add the image to the overlay
        overlay.add_overlay(image)

        # Create a label to display in front of the image
        label = Gtk.Label(label="Hello guys! I'm here to assist you")
        label.set_halign(Gtk.Align.CENTER)
        label.set_valign(Gtk.Align.CENTER)
        label.set_margin_top(50)  # Adjust margin as needed
        label.set_margin_bottom(50)
        label.set_margin_start(20)
        label.set_margin_end(20)

        # Add the label to the overlay
        overlay.add_overlay(label)

        # Set the overlay as the window's child
        window.set_child(overlay)

        # Present the window
        window.present()

# Create and run the application
app = MyApplication()
exit_status = app.run(sys.argv)
sys.exit(exit_status)
