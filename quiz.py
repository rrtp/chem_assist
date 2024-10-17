import gi
import sqlite3

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class QuestionApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Question App")
        self.set_default_size(400, 300)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        self.question_label = Gtk.Label(label="")
        self.box.append(self.question_label)

        self.option_buttons = []
        for i in range(4):
            button = Gtk.Button(label="")
            button.connect("clicked", self.on_option_clicked)
            self.option_buttons.append(button)
            self.box.append(button)

        self.load_question()

    def load_question(self):
        conn = sqlite3.connect('questions.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM questions ORDER BY RANDOM() LIMIT 1")
        question = cursor.fetchone()
        
        if question:
            self.question_label.set_text(question[1])
            for i in range(4):
                self.option_buttons[i].set_label(question[i + 2])
        
        conn.close()

    def on_option_clicked(self, button):
        print(f"You clicked: {button.get_label()}")

app = QuestionApp()
app.connect("destroy", Gtk.main_quit)
app.show()
Gtk.main()
