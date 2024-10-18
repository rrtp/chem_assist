import gi
import sqlite3
from gi.repository import Gtk, GLib

gi.require_version("Gtk", "4.0")

class QuizApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="HELLO QUIZ")
        self.set_default_size(400, 300)

        self.score = 0
        self.current_question_index = 0
        self.questions = self.load_questions()

        self.grid = Gtk.Grid()
        self.add(self.grid)

        self.question_label = Gtk.Label()
        self.grid.attach(self.question_label, 0, 0, 1, 1)

        self.options = []
        for i in range(4):
            button = Gtk.Button(label="")
            button.connect("clicked", self.on_option_clicked, i)
            self.grid.attach(button, 0, i + 1, 1, 1)
            self.options.append(button)

        self.load_question()

    def load_questions(self):
        conn = sqlite3.connect('DATABASEname')
        cursor = conn.cursor()
        cursor.execute("SELECT question, option1, option2, option3, option4, answer FROM questions")
        questions = cursor.fetchall()
        conn.close()
        return questions

    def load_question(self):
        if self.current_question_index < len(self.questions):
            question_data = self.questions[self.current_question_index]
            self.question_label.set_text(question_data[0])
            for i in range(4):
                self.options[i].set_label(question_data[i + 1])
        else:
            self.question_label.set_text(f" Finished! Your score: {self.score}/{len(self.questions)}")
            for button in self.options:
                button.set_sensitive(False)

    def on_option_clicked(self, button, selected_index):
        correct_answer = self.questions[self.current_question_index][5]
        if selected_index == correct_answer - 1:
            self.score += 1
        self.current_question_index += 1
        self.load_question()

if __name__ == "__main__":
    app = HELLO QUIZ()
    app.connect("destroy", Gtk.main_quit)
    app.show()
    Gtk.main()
