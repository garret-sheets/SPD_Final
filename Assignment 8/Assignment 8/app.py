import os

from flask import Flask, render_template, request, redirect
import sqlite3


def initialize_db():
    conn = sqlite3.connect('birthdays.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS birthdays (
           id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            month INTEGER NOT NULL,
            day INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


initialize_db()

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        month = request.form.get('month')
        day = request.form.get('day')

        conn = sqlite3.connect('birthdays.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?)", (name, month, day))
        conn.commit()
        conn.close()

        return redirect('/')
    else:
        # Handle GET request
        conn = sqlite3.connect('birthdays.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, month || '-' || day as birthday FROM birthdays")
        birthdays = cursor.fetchall()
        conn.close()
        return render_template('index.html', birthdays=birthdays)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    conn = sqlite3.connect('birthdays.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM birthdays WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = sqlite3.connect('birthdays.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        month = request.form.get('month')
        day = request.form.get('day')
        cursor.execute("UPDATE birthdays SET name=?, month=?, day=? WHERE id=?", (name, month, day, id))
        conn.commit()
        conn.close()
        return redirect('/')
    else:
        cursor.execute("SELECT name, month, day FROM birthdays WHERE id=?", (id,))
        birthday = cursor.fetchone()
        conn.close()
        return render_template('edit.html', id=id, birthday=birthday)

if __name__ == "__main__":
    app.run()
