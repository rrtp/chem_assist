import gi
import sqlite3

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

class Quiz(Gtk.Window):
    def __init__(self):
        super().__init__(title="Quiz!!!")
        self.set_default_size(400, 300)

        self.question_label = Gtk.Label()
        self.option_buttons = []

        self.quiz_data = self.load_questions()

        self.current_question = 0
        self.score = 0

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(self.box)

        self.box.append(self.question_label)
        
        for i in range(4):  # Assuming 4 options for each question
            button = Gtk.Button(label="")
            button.connect("clicked", self.on_option_clicked, i)
            self.option_buttons.append(button)
            self.box.append(button)

        self.show_question()

    def load_questions(self):
        connection = sqlite3.connect('DATABASEname')
        cursor = connection.cursor()
        cursor.execute("SELECT question, option1, option2, option3, option4, answer FROM questions")
        questions = cursor.fetchall()
        connection.close()
        return questions

    def show_question(self):
        if self.current_question < len(self.quiz_data):
            question_data = self.quiz_data[self.current_question]
            self.question_label.set_text(question_data[0])

            for i in range(4):
                self.option_buttons[i].set_label(question_data[i + 1])
                self.option_buttons[i].set_sensitive(True)

        else:
            self.show_score()

    def on_option_clicked(self, button, option_index):
        selected_option = self.option_buttons[option_index].get_label()
        if selected_option == self.quiz_data[self.current_question][5]:  # answer is in the last column
            self.score += 1

        self.current_question += 1
        self.show_question()

    def show_score(self):
        self.question_label.set_text(f"Quiz finished! Your score: {self.score}/{len(self.quiz_data)}")
        for button in self.option_buttons:
            button.set_sensitive(False)

if __name__ == "__main__":
    app = Quiz()
    app.connect("destroy", Gtk.main_quit)
    app.show()
    Gtk.main()
