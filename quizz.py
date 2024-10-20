import sqlite3
import random
import gi

gi.require_version('Gtk', '4.0')
from gi.repository import Gtk

class QuizWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Quiz App")
        self.set_default_size(400, 300)

        # Initialize score
        self.score = 0

        # Create a box to hold the widgets
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.set_child(self.box)

        # Load questions from the database
        self.questions = self.load_questions()
        random.shuffle(self.questions)  # Shuffle the questions

        # Create a label for questions
        self.question_label = Gtk.Label(label="")
        self.box.append(self.question_label)

        # Create a label for score
        self.score_label = Gtk.Label(label="Score: 0")
        self.box.append(self.score_label)

        # Create buttons for options
        self.option_buttons = []
        for i in range(4):  # Four options (A, B, C, D)
            button = Gtk.Button(label="")
            button.connect("clicked", self.on_option_clicked, i)
            self.option_buttons.append(button)
            self.box.append(button)

        # Initialize current question index
        self.current_question_index = 0
        self.load_question(self.current_question_index)

        # Connect the destroy event to quit the application
        self.connect("destroy", Gtk.Application)  # Corrected line

    def load_questions(self):
        conn = sqlite3.connect('quiz.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM questions")
        questions = cursor.fetchall()
        conn.close()
        return questions

    def load_question(self, index):
        if index < len(self.questions):
            question = self.questions[index]
            self.question_label.set_text(question[1])  # question text

            # Set the options
            self.option_buttons[0].set_label(question[2])  # option A
            self.option_buttons[1].set_label(question[3])  # option B
            self.option_buttons[2].set_label(question[4])  # option C
            self.option_buttons[3].set_label(question[5])  # option D
        else:
            self.question_label.set_text("Quiz finished!")
            self.score_label.set_text(f"Final Score: {self.score}")  # Show final score
            for button in self.option_buttons:
                button.set_sensitive(False)  # Disable buttons

    def on_option_clicked(self, button, option_index):
        correct_answer = self.questions[self.current_question_index][6]
        selected_answer = self.option_buttons[option_index].get_label()

        if selected_answer == correct_answer:
            print("Correct!")
            self.score += 1  # Increment score for a correct answer
        else:
            print("Wrong!")

        # Update score label
        self.score_label.set_text(f"Score: {self.score}")

        # Remove the answered question from the list
        self.questions.pop(self.current_question_index)

        # Load the next question
        if len(self.questions) > 0:
            self.load_question(self.current_question_index)
        else:
            print("Quiz finished!")
            self.load_question(self.current_question_index)  # Load finish message

class QuizApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="com.example.QuizApp")

    def do_activate(self):
        # Create and show the quiz window
        quiz_window = QuizWindow()
        quiz_window.present()

if __name__ == "__main__":
    app = QuizApp()
    app.run()
