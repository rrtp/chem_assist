import mysql.connector
import tkinter as tk
from tkinter import messagebox, ttk

def create_connection():
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host='localhost',       # MySQL server details
        user='root',           # MySQL username
        password='Login@4475', # MySQL password
        database='quiz_app'    # Update with your database name if needed
    )
    return connection

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

    # Create a treeview to display user scores
    tree = ttk.Treeview(report_window, columns=("Name", "Score"), show='headings')
    tree.heading("Name", text="Name")
    tree.heading("Score", text="Score")
    tree.pack(fill=tk.BOTH, expand=True)

    # Fetch user scores from the database
    cursor = connection.cursor()
    cursor.execute('SELECT name, score FROM users')
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

    # Report button
    report_button = tk.Button(root, text="Show Report", command=lambda: show_report(connection), font=("Arial", 12), bg="#0288d1", fg="white")
    report_button.pack(pady=10)

    # Exit button
    exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 12), bg="#f44336", fg="white")
    exit_button.pack(pady=10)

def main():
    global root, connection
    # Connect to the database and create tables
    connection = create_connection()
    create_tables(connection)
    add_sample_questions(connection)
    
    # Set up the main window
    root = tk.Tk()
    root.title("Chemistry Quiz Application")
    root.attributes('-fullscreen', True)  # Open in full screen
    root.configure(bg="#e0f7fa")  # Light blue background

    reset_app()  # Load the home screen

    # Run the Tkinter event loop
    root.mainloop()

    # Close the database connection when the program ends
    connection.close()

if __name__ == '__main__':
    main()