import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk

def create_tables(connection):
    # Create tables if they don't exist
    with connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                score INT NOT NULL
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quiz_questions (
                question_id INT AUTO_INCREMENT PRIMARY KEY,
                question TEXT NOT NULL,
                option_a VARCHAR(255) NOT NULL,
                option_b VARCHAR(255) NOT NULL,
                option_c VARCHAR(255) NOT NULL,
                option_d VARCHAR(255) NOT NULL,
                correct_answer CHAR(1) NOT NULL
            );
        ''')
        # New table for user-submitted questions
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_questions (
                question_id INT AUTO_INCREMENT PRIMARY KEY,
                question TEXT NOT NULL,
                option_a VARCHAR(255) NOT NULL,
                option_b VARCHAR(255) NOT NULL,
                option_c VARCHAR(255) NOT NULL,
                option_d VARCHAR(255) NOT NULL,
                correct_answer CHAR(1) NOT NULL
            );
        ''')
    connection.commit()

def add_sample_questions(connection):
    # Add 10 chemistry questions for 12th-grade level
    sample_questions = [
        ("Which of the following is a Lewis acid?", "NH3", "BF3", "H2O", "CH4", "B"),
        ("What is the IUPAC name of acetone?", "Propan-2-one", "Butanone", "Methanone", "Ethanal", "A"),
        ("Which element has the highest electronegativity?", "Oxygen", "Fluorine", "Chlorine", "Nitrogen", "B"),
        ("The bond order of O2 is:", "1", "2", "3", "2.5", "B"),
        ("What is the main component of natural gas?", "Methane", "Ethane", "Propane", "Butane", "A"),
        ("Which is the most stable allotrope of carbon?", "Graphite", "Diamond", "Fullerene", "Carbon Nanotubes", "A"),
        ("What is the pH of a 0.01 M HCl solution?", "2", "1", "3", "4", "A"),
        ("Which of the following is an example of a homogeneous mixture?", "Sand and salt", "Oil and water", "Air", "Iron filings and sulfur", "C"),
        ("What is the oxidation state of sulfur in H2SO4?", "+6", "+4", "+2", "0", "A"),
        ("Which of the following undergoes nucleophilic substitution reactions?", "Alkene", "Alkyne", "Haloalkane", "Aromatic compound", "C"),
    ]
    
    with connection.cursor() as cursor:
        cursor.executemany('''
            INSERT INTO quiz_questions (question, option_a, option_b, option_c, option_d, correct_answer)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', sample_questions)
    connection.commit()

def show_results(user_name, score, total_questions, connection):
    # Store user score in the database
    with connection.cursor() as cursor:
        cursor.execute('INSERT INTO users (name, score) VALUES (%s, %s)', (user_name, score))
    connection.commit()

    # Clear the main window and show results
    for widget in root.winfo_children():
        widget.destroy()

    # Display the student's name and score
    result_label = tk.Label(root, text=f"Quiz Results for {user_name}", font=("Arial", 16, "bold"), bg="#e0f7fa")
    result_label.pack(pady=20)

    score_label = tk.Label(root, text=f"Score: {score}/{total_questions}", font=("Arial", 14), bg="#e0f7fa")
    score_label.pack(pady=10)

    percentage = (score / total_questions) * 100
    percentage_label = tk.Label(root, text=f"Percentage: {percentage:.2f}%", font=("Arial", 14), bg="#e0f7fa")
    percentage_label.pack(pady=10)

    # Home and Exit buttons
    home_button = tk.Button(root, text="Home", command=reset_app, bg="#0288d1", fg="white", font=("Arial", 12))
    home_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.quit, bg="#f44336", fg="white", font=("Arial", 12))
    exit_button.pack(pady=10)

def show_report(connection):
    # Create a new window for the report
    report_window = tk.Toplevel(root)
    report_window.title("User Report")
    report_window.geometry("400x300")

    # Create a treeview to display user scores in descending order
    tree = ttk.Treeview(report_window, columns=("Name", "Score"), show='headings')
    tree.heading("Name", text="Name")
    tree.heading("Score", text="Score")
    tree.pack(fill=tk.BOTH, expand=True)

    # Fetch user scores from the database in descending order
    cursor = connection.cursor()
    cursor.execute('SELECT name, score FROM users ORDER BY score DESC')
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

    # Close button for report window
    close_button = tk.Button(report_window, text="Close", command=report_window.destroy)
    close_button.pack(pady=10)


def start_quiz_window(connection, user_name):
    # Fetch all quiz questions from the database
    cursor = connection.cursor()
    cursor.execute('SELECT question, option_a, option_b, option_c, option_d, correct_answer FROM quiz_questions LIMIT 10')
    questions = cursor.fetchall()
    cursor.close()

    # Track the current question index and score
    current_question = [0]
    score = [0]

    # Initialize StringVar for radio buttons
    var = tk.StringVar(value="")  # No default selection

    def show_question():
        # Get the current question
        if current_question[0] < len(questions):
            question = questions[current_question[0]]

            # Clear the window
            for widget in root.winfo_children():
                widget.destroy()

            # Display the current question number
            question_number_label = tk.Label(root, text=f"Question {current_question[0] + 1}/{len(questions)}", font=("Arial", 14), bg="#e0f7fa")
            question_number_label.pack(pady=10)

            # Display the question and options
            question_label = tk.Label(root, text=question[0], font=("Arial", 14), wraplength=400, bg="#e0f7fa")
            question_label.pack(pady=10)

            # Create radio buttons for each option
            for idx, option in enumerate(question[1:5], start=1):
                tk.Radiobutton(root, text=option, variable=var, value=chr(64 + idx), font=("Arial", 12), bg="#e0f7fa").pack(anchor='w')

            # Function to check the answer and move to the next question
            def next_question():
                if var.get() == "":
                    messagebox.showerror("Error", "Please select an answer before proceeding to the next question.")
                else:
                    if var.get() == question[5]:
                        score[0] += 1
                    current_question[0] += 1
                    var.set("")  # Reset the radio button selection
                    show_question()

            # Next button
            next_button = tk.Button(root, text="Next", command=next_question, bg="#0288d1", fg="white", font=("Arial", 12))
            next_button.pack(pady=20)
        else:
            # Show results in the main window
            show_results(user_name, score[0], len(questions), connection)

    # Create the quiz window
    show_question()

def reset_app():
    # Clear the main window and go back to the home screen
    for widget in root.winfo_children():
        widget.destroy()
    
    # Get the user's name
    name_label = tk.Label(root, text="Enter your name:", font=("Arial", 12), bg="#e0f7fa")
    name_label.pack(pady=10)
    name_entry = tk.Entry(root, font=("Arial", 12))
    name_entry.pack(pady=5)

    # Start quiz button
    def start_quiz():
        user_name = name_entry.get()
        if user_name and user_name.isalpha():
            start_quiz_window(connection, user_name)
            name_entry.delete(0, tk.END)  # Clear the entry box
        else:
            messagebox.showerror("Error", "Please enter a valid name (only letters).")

    start_button = tk.Button(root, text="Start Quiz", command=start_quiz, font=("Arial", 12), bg="#0288d1", fg="white")
    start_button.pack(pady=10)

    # Show report button
    report_button = tk.Button(root, text="User Report", command=lambda: show_report(connection), font=("Arial", 12), bg="#4caf50", fg="white")
    report_button.pack(pady=5)

    # User options button
    user_button = tk.Button(root, text="User Options", command=lambda: admin_options(connection), font=("Arial", 12), bg="#9c27b0", fg="white")
    user_button.pack(pady=5)

def admin_options(connection):
    # Create a new window for user options
    admin_window = tk.Toplevel(root)
    admin_window.title("User Options")
    admin_window.geometry("300x200")

    # Buttons to add and remove questions
    tk.Button(admin_window, text="Add Question", command=lambda: add_question_window(connection)).pack(pady=10)
    tk.Button(admin_window, text="Remove Question", command=lambda: remove_question_window(connection)).pack(pady=10)
    tk.Button(admin_window, text="Close", command=admin_window.destroy).pack(pady=10)

def add_question_window(connection):
    # Create a new window for adding questions
    add_window = tk.Toplevel(root)
    add_window.title("Add Question")
    add_window.geometry("400x400")
    
    # Labels and entries for the question and options
    tk.Label(add_window, text="Question:").pack()
    question_entry = tk.Entry(add_window, width=50)
    question_entry.pack()

    tk.Label(add_window, text="Option A:").pack()
    option_a_entry = tk.Entry(add_window, width=50)
    option_a_entry.pack()

    tk.Label(add_window, text="Option B:").pack()
    option_b_entry = tk.Entry(add_window, width=50)
    option_b_entry.pack()

    tk.Label(add_window, text="Option C:").pack()
    option_c_entry = tk.Entry(add_window, width=50)
    option_c_entry.pack()

    tk.Label(add_window, text="Option D:").pack()
    option_d_entry = tk.Entry(add_window, width=50)
    option_d_entry.pack()

    tk.Label(add_window, text="Correct Answer (A, B, C, or D):").pack()
    correct_answer_entry = tk.Entry(add_window, width=10)
    correct_answer_entry.pack()

def admin_options(connection):
    # Create a new window for user options
    admin_window = tk.Toplevel(root)
    admin_window.title("User Options")
    admin_window.geometry("300x300")

    # Buttons for user options
    tk.Button(admin_window, text="Add Question", command=lambda: add_question_window(connection)).pack(pady=10)
    tk.Button(admin_window, text="Remove Question", command=lambda: remove_question_window(connection)).pack(pady=10)
    tk.Button(admin_window, text="Play User Quiz", command=lambda: enter_user_name_for_user_quiz(connection)).pack(pady=10)
    tk.Button(admin_window, text="Show User Quiz Scores", command=lambda: show_user_quiz_scores(connection)).pack(pady=10)
    tk.Button(admin_window, text="Close", command=admin_window.destroy).pack(pady=10)

def enter_user_name_for_user_quiz(connection):
    # Prompt the user to enter their name
    name_window = tk.Toplevel(root)
    name_window.title("Enter Your Name")
    name_window.geometry("300x150")

    tk.Label(name_window, text="Enter your name:", font=("Arial", 12)).pack(pady=10)
    name_entry = tk.Entry(name_window, font=("Arial", 12))
    name_entry.pack(pady=5)

    def start_user_quiz():
        user_name = name_entry.get().strip()
        if user_name and user_name.isalpha():
            start_user_quiz_window(connection, user_name)
            name_window.destroy()  # Close the name entry window
        else:
            messagebox.showerror("Error", "Please enter a valid name (only letters).")

    start_button = tk.Button(name_window, text="Start User Quiz", command=start_user_quiz, font=("Arial", 12), bg="#0288d1", fg="white")
    start_button.pack(pady=10)

def start_user_quiz_window(connection, user_name):
    # Fetch all user-submitted quiz questions from the database
    cursor = connection.cursor()
    cursor.execute('SELECT question, option_a, option_b, option_c, option_d, correct_answer FROM user_questions LIMIT 10')
    questions = cursor.fetchall()
    cursor.close()

    # If no user questions are available
    if not questions:
        messagebox.showinfo("Info", "No user-submitted questions available!")
        return

    # Track the current question index and score
    current_question = [0]
    score = [0]
    var = tk.StringVar(value="")

    def show_question():
        if current_question[0] < len(questions):
            question = questions[current_question[0]]
            for widget in root.winfo_children():
                widget.destroy()

            question_number_label = tk.Label(root, text=f"User Quiz - Question {current_question[0] + 1}/{len(questions)}", font=("Arial", 14), bg="#e0f7fa")
            question_number_label.pack(pady=10)

            question_label = tk.Label(root, text=question[0], font=("Arial", 14), wraplength=400, bg="#e0f7fa")
            question_label.pack(pady=10)

            for idx, option in enumerate(question[1:5], start=1):
                tk.Radiobutton(root, text=option, variable=var, value=chr(64 + idx), font=("Arial", 12), bg="#e0f7fa").pack(anchor='w')

            def next_question():
                if var.get() == "":
                    messagebox.showerror("Error", "Please select an answer before proceeding to the next question.")
                else:
                    if var.get() == question[5]:
                        score[0] += 1
                    current_question[0] += 1
                    var.set("")
                    show_question()

            next_button = tk.Button(root, text="Next", command=next_question, bg="#0288d1", fg="white", font=("Arial", 12))
            next_button.pack(pady=20)
        else:
            show_results(user_name, score[0], len(questions), connection, is_user_quiz=True)

    show_question()

def show_results(user_name, score, total_questions, connection, is_user_quiz=False):
    # Store user score in the user_quiz_scores table if it’s a user-submitted quiz
    with connection.cursor() as cursor:
        if is_user_quiz:
            cursor.execute('INSERT INTO user_quiz_scores (name, score) VALUES (%s, %s)', (user_name, score))
        else:
            cursor.execute('INSERT INTO users (name, score) VALUES (%s, %s)', (user_name, score))
    connection.commit()

    for widget in root.winfo_children():
        widget.destroy()

    result_label = tk.Label(root, text=f"Quiz Results for {user_name}", font=("Arial", 16, "bold"), bg="#e0f7fa")
    result_label.pack(pady=20)

    score_label = tk.Label(root, text=f"Score: {score}/{total_questions}", font=("Arial", 14), bg="#e0f7fa")
    score_label.pack(pady=10)

    percentage = (score / total_questions) * 100
    percentage_label = tk.Label(root, text=f"Percentage: {percentage:.2f}%", font=("Arial", 14), bg="#e0f7fa")
    percentage_label.pack(pady=10)

    home_button = tk.Button(root, text="Home", command=reset_app, bg="#0288d1", fg="white", font=("Arial", 12))
    home_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=root.quit, bg="#f44336", fg="white", font=("Arial", 12))
    exit_button.pack(pady=10)

def show_user_quiz_scores(connection):
    # Create a new window for displaying user quiz scores
    score_window = tk.Toplevel(root)
    score_window.title("User Quiz Scores")
    score_window.geometry("400x300")

    # Treeview to display scores
    tree = ttk.Treeview(score_window, columns=("Name", "Score"), show='headings')
    tree.heading("Name", text="Name")
    tree.heading("Score", text="Score")
    tree.pack(fill=tk.BOTH, expand=True)

    # Fetch scores from the user_quiz_scores table in descending order
    cursor = connection.cursor()
    cursor.execute('SELECT name, score FROM user_quiz_scores ORDER BY score DESC')
    for row in cursor.fetchall():
        tree.insert("", tk.END, values=row)

    # Close button for the score window
    close_button = tk.Button(score_window, text="Close", command=score_window.destroy)
    close_button.pack(pady=10)

def create_tables(connection):
    # Create tables if they don't exist, including a new table for user quiz scores
    with connection.cursor() as cursor:
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            score INT NOT NULL
        );''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS quiz_questions (
            question_id INT AUTO_INCREMENT PRIMARY KEY,
            question TEXT NOT NULL,
            option_a VARCHAR(255) NOT NULL,
            option_b VARCHAR(255) NOT NULL,
            option_c VARCHAR(255) NOT NULL,
            option_d VARCHAR(255) NOT NULL,
            correct_answer CHAR(1) NOT NULL
        );''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_questions (
            question_id INT AUTO_INCREMENT PRIMARY KEY,
            question TEXT NOT NULL,
            option_a VARCHAR(255) NOT NULL,
            option_b VARCHAR(255) NOT NULL,
            option_c VARCHAR(255) NOT NULL,
            option_d VARCHAR(255) NOT NULL,
            correct_answer CHAR(1) NOT NULL
        );''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_quiz_scores (
            score_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            score INT NOT NULL
        );''')
    connection.commit()

def add_question_window(connection):
    # Create a new window for adding questions
    add_window = tk.Toplevel(root)
    add_window.title("Add Question")
    add_window.geometry("400x400")
    
    # Labels and entries for the question and options
    tk.Label(add_window, text="Question:").pack()
    question_entry = tk.Entry(add_window, width=50)
    question_entry.pack()

    tk.Label(add_window, text="Option A:").pack()
    option_a_entry = tk.Entry(add_window, width=50)
    option_a_entry.pack()

    tk.Label(add_window, text="Option B:").pack()
    option_b_entry = tk.Entry(add_window, width=50)
    option_b_entry.pack()

    tk.Label(add_window, text="Option C:").pack()
    option_c_entry = tk.Entry(add_window, width=50)
    option_c_entry.pack()

    tk.Label(add_window, text="Option D:").pack()
    option_d_entry = tk.Entry(add_window, width=50)
    option_d_entry.pack()

    tk.Label(add_window, text="Correct Answer (A, B, C, or D):").pack()
    correct_answer_entry = tk.Entry(add_window, width=10)
    correct_answer_entry.pack()

    def add_question_to_db():
        # Fetch input values
        question = question_entry.get().strip()
        option_a = option_a_entry.get().strip()
        option_b = option_b_entry.get().strip()
        option_c = option_c_entry.get().strip()
        option_d = option_d_entry.get().strip()
        correct_answer = correct_answer_entry.get().strip().upper()

        # Validation
        if not (question and option_a and option_b and option_c and option_d and correct_answer):
            messagebox.showerror("Error", "All fields are required.")
            return
        
        if correct_answer not in ("A", "B", "C", "D"):
            messagebox.showerror("Error", "Correct answer must be one of A, B, C, or D.")
            return
        
        # Add the question to the database
        with connection.cursor() as cursor:
            cursor.execute('''
                INSERT INTO user_questions (question, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (question, option_a, option_b, option_c, option_d, correct_answer))
        connection.commit()

        messagebox.showinfo("Success", "Question added successfully!")
        add_window.destroy()  # Close the window

    # Add Question button
    add_button = tk.Button(add_window, text="Add Question", command=add_question_to_db, bg="#4caf50", fg="white", font=("Arial", 12))
    add_button.pack(pady=10)

    # Cancel button
    cancel_button = tk.Button(add_window, text="Cancel", command=add_window.destroy, bg="#f44336", fg="white", font=("Arial", 12))
    cancel_button.pack(pady=10)


def remove_question_window(connection):
    # Create a new window for removing questions
    remove_window = tk.Toplevel(root)
    remove_window.title("Remove User-Submitted Question")
    remove_window.geometry("500x400")

    # Create a Treeview to display questions
    tree = ttk.Treeview(remove_window, columns=("ID", "Question"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Question", text="Question")
    tree.column("ID", width=50)
    tree.column("Question", width=400)
    tree.pack(fill=tk.BOTH, expand=True)

    # Fetch questions from the user_questions table
    cursor = connection.cursor()
    cursor.execute("SELECT question_id, question FROM user_questions")
    questions = cursor.fetchall()
    cursor.close()

    # Insert each question into the Treeview
    for question in questions:
        tree.insert("", tk.END, values=question)

    def remove_question():
        selected_item = tree.selection()
        if selected_item:
            question_id = tree.item(selected_item)["values"][0]

            # Confirm deletion
            confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this question?")
            if confirm:
                cursor = connection.cursor()
                cursor.execute("DELETE FROM user_questions WHERE question_id = %s", (question_id,))
                connection.commit()
                cursor.close()

                # Remove question from Treeview
                tree.delete(selected_item)
                messagebox.showinfo("Success", "Question removed successfully!")
        else:
            messagebox.showwarning("Warning", "Please select a question to remove.")

    # Remove button
    remove_button = tk.Button(remove_window, text="Remove Selected Question", command=remove_question, bg="#f44336", fg="white", font=("Arial", 12))
    remove_button.pack(pady=10)

    # Close button
    close_button = tk.Button(remove_window, text="Close", command=remove_window.destroy, bg="#0288d1", fg="white", font=("Arial", 12))
    close_button.pack(pady=10)

def main(db_connection):
    # Main application setup
    global root
    global connection
    root = tk.Tk()
    root.title("Quiz Application")
    root.geometry("600x400")
    root.configure(bg="#e0f7fa")

    # Database setup
    connection=db_connection
    create_tables(connection)
    add_sample_questions(connection)  # Add sample questions

    reset_app()  # Start the home screen

    root.mainloop()