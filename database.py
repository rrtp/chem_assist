import sqlite3

# Connect to the database (or create it)
conn = sqlite3.connect('quiz.db')
cursor = conn.cursor()

# Create a table for questions with options
cursor.execute('''
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    option_a TEXT NOT NULL,
    option_b TEXT NOT NULL,
    option_c TEXT NOT NULL,
    option_d TEXT NOT NULL,
    answer TEXT NOT NULL
)
''')

# Insert sample questions
cursor.execute("INSERT INTO questions (question, option_a, option_b, option_c, option_d, answer) VALUES ('which of the following is a primary alcohol?', '2-propanol', 'methanol', '2-butanol', 'tertiary butyl alcohol','methanol')")
cursor.execute("INSERT INTO questions (question, option_a, option_b, option_c, option_d, answer) VALUES ('which of the following oxides is amphoteric in nature?', 'Na2O', 'CO2', 'Al2O3', 'SO2', 'Al2O3')")
cursor.execute("INSERT INTO questions (question, option_a, option_b, option_c, option_d, answer) VALUES ('which of the following is the strongest acid?', 'HCL', 'H2SO4', 'HNO3', 'HClO4', 'HClO4')")

# Commit changes and close the connection
conn.commit()
conn.close()
