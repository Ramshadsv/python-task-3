import sqlite3
from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key_change_in_production'
DATABASE = 'database.db'


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL)''')
    db.execute('''CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        course TEXT NOT NULL)''')
    db.commit()
    db.close()


@app.route('/')
def index():
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        if not username or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')
        hashed = generate_password_hash(password)
        db = get_db()
        try:
            db.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed))
            db.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.', 'error')
        finally:
            db.close()
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        db.close()
        if user and check_password_hash(user['password'], password):
            session['user'] = username
            flash('Welcome back, ' + username + '!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    total = db.execute('SELECT COUNT(*) FROM students').fetchone()[0]
    db.close()
    return render_template('dashboard.html', username=session['user'], total=total)

@app.route('/students')
def students():
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    data = db.execute('SELECT * FROM students ORDER BY id DESC').fetchall()
    db.close()
    return render_template('students.html', students=data)

@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    if 'user' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        name   = request.form['name'].strip()
        email  = request.form['email'].strip()
        course = request.form['course'].strip()
        if not name or not email or not course:
            flash('All fields are required.', 'error')
            return render_template('add_student.html')
        db = get_db()
        db.execute('INSERT INTO students (name, email, course) VALUES (?, ?, ?)', (name, email, course))
        db.commit()
        db.close()
        flash('Student added successfully!', 'success')
        return redirect(url_for('students'))
    return render_template('add_student.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    student = db.execute('SELECT * FROM students WHERE id = ?', (id,)).fetchone()
    if not student:
        db.close()
        flash('Student not found.', 'error')
        return redirect(url_for('students'))
    if request.method == 'POST':
        name   = request.form['name'].strip()
        email  = request.form['email'].strip()
        course = request.form['course'].strip()
        db.execute('UPDATE students SET name=?, email=?, course=? WHERE id=?', (name, email, course, id))
        db.commit()
        db.close()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('students'))
    db.close()
    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    db = get_db()
    db.execute('DELETE FROM students WHERE id=?', (id,))
    db.commit()
    db.close()
    flash('Student deleted.', 'info')
    return redirect(url_for('students'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
