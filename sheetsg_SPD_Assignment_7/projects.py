import sqlite3
import os  # Import the os module to use the absolute path

# Get the absolute path of your project's root directory
root_path = os.path.abspath(os.path.dirname(__file__))

# Absolute path to the database file
db_path = os.path.join(root_path, "projects.db")

class ProjectDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(db_path)  # Use the db_path here
        self.cursor = self.conn.cursor()
        self.create_table()  # You can create the table on initialization

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY,
                title TEXT,
                description TEXT,
                start_date TEXT,
                end_date TEXT
            )
        ''')
        self.conn.commit()

    def add_project(self, title, description, start_date, end_date):
        self.cursor.execute('''
            INSERT INTO projects (title, description, start_date, end_date)
            VALUES (?, ?, ?, ?)
        ''', (title, description, start_date, end_date))
        self.conn.commit()

    def get_projects(self):
        self.cursor.execute('SELECT * FROM projects')
        return self.cursor.fetchall()

    def get_project_by_id(self, project_id):
        self.cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
        return self.cursor.fetchone()

    def update_project(self, project_id, title, description, start_date, end_date):
        self.cursor.execute('''
            UPDATE projects
            SET title = ?, description = ?, start_date = ?, end_date = ?
            WHERE id = ?
        ''', (title, description, start_date, end_date, project_id))
        self.conn.commit()

    def delete_project(self, project_id):
        self.cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()