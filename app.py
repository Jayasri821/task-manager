from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secretkey"

# DATABASE

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# USERS TABLE

cursor.execute('''
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT
)
''')

# TASKS TABLE

cursor.execute('''
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
task TEXT,
priority TEXT,
due_date TEXT,
status TEXT
)
''')

conn.commit()
conn.close()

# HOME PAGE

@app.route('/')
def home():

    if 'user' not in session:
        return redirect('/login')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM tasks WHERE username=?",
        (session['user'],)
    )

    tasks = cursor.fetchall()

    conn.close()

    return render_template(
        'index.html',
        tasks=tasks
    )

# REGISTER

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO users
            (username, password)

            VALUES (?, ?)
            ''',

            (username, password)
        )

        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

# LOGIN

@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            '''
            SELECT * FROM users
            WHERE username=? AND password=?
            ''',

            (username, password)
        )

        user = cursor.fetchone()

        conn.close()

        if user:

            session['user'] = username

            return redirect('/')

    return render_template('login.html')

# LOGOUT

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect('/login')

# ADD TASK

@app.route('/add', methods=['POST'])
def add():

    if 'user' not in session:
        return redirect('/login')

    task = request.form['task']
    priority = request.form['priority']
    due_date = request.form['due_date']

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO tasks
        (username, task, priority, due_date, status)

        VALUES (?, ?, ?, ?, ?)
        ''',

        (
            session['user'],
            task,
            priority,
            due_date,
            "Pending"
        )
    )

    conn.commit()
    conn.close()

    return redirect('/')

# COMPLETE TASK

@app.route('/complete/<int:id>')
def complete(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        UPDATE tasks
        SET status='Completed'
        WHERE id=?
        ''',

        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

# DELETE TASK

@app.route('/delete/<int:id>')
def delete(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        '''
        DELETE FROM tasks
        WHERE id=?
        ''',

        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)