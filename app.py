from flask import Flask, render_template, request, redirect, flash
import sqlite3
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex(16)

def init_db():
    with sqlite3.connect('student.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                roll INTEGER NOT NULL UNIQUE,
                name TEXT NOT NULL
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect('student.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT roll, name FROM students')
        students = cursor.fetchall()
    return render_template('index.html', students=students)

@app.route('/submit', methods=['POST'])
def submit():
    roll = request.form['roll']
    name = request.form['name']

    with sqlite3.connect('student.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO students (roll, name) VALUES (?, ?)', (roll, name))
            conn.commit()
            flash('Student added successfully!', 'success')
        except sqlite3.IntegrityError:
            flash('Roll number already exists!', 'error')

    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
