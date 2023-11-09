from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

# Get the absolute path of your project's root directory
root_path = os.path.abspath(os.path.dirname(__file__))

# Define the absolute path to your database
db_path = os.path.join(root_path, "projects.db")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/projects')
def my_projects():
    # Connect to the database using the absolute path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Retrieve project data from the database
    cursor.execute("SELECT Title, Description, ImageFileName FROM projects")
    projects_data = cursor.fetchall()

    # Close the database connection
    conn.close()

    return render_template("projects.html", projects=projects_data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/form')
def register():
    return render_template('form.html')

@app.route('/confirmation')
def confirmation():
    return render_template('confirmation.html')

# Add a new route to handle project submission
@app.route('/add_project', methods=['POST'])
def add_project():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        image_filename = request.form.get('image_filename')

        # Connect to the database using the absolute path
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Insert the new project into the database
        cursor.execute("INSERT INTO projects (Title, Description, ImageFileName) VALUES (?, ?, ?)",
                       (title, description, image_filename))
        conn.commit()
        conn.close()

        # Redirect to the Projects page to view the newly added project
        return redirect(url_for('my_projects'))

    # Create a route to display the delete confirmation page for a specific project
@app.route('/delete_project/<int:project_id>')
def delete_project(project_id):
    # Connect to the database using the absolute path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Retrieve project data from the database
    cursor.execute("SELECT id, title, description, image_filename FROM projects WHERE id = ?", (project_id,))
    project = cursor.fetchone()

    # Close the database connection
    conn.close()

    if project:
        return render_template("delete.html", project=project)
    else:
        flash("Project not found", "danger")
        return redirect(url_for("projects"))

# Create a route to handle the actual project deletion
@app.route('/delete_project/<int:project_id>', methods=["POST"])
def delete_project_confirm(project_id):
    # Connect to the database using the absolute path
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Delete the project from the database
    cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
    conn.commit()

    # Close the database connection
    conn.close()

    flash("Project deleted successfully", "success")
    return redirect(url_for("projects"))

if __name__ == '__main__':
    app.run(debug=True)