from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'student_crud_secret_key_change_me_in_production'

# Use absolute path to ensure connection is always made to the project's database
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'students.db')

def get_db_connection():
    """Establishes connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database and creates the students table if it doesn't exist."""
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            phone TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route('/')
def index():
    """Main single-page view showing the CRUD form and the student table list."""
    edit_id = request.args.get('edit', '').strip()
    edit_student = None
    
    conn = get_db_connection()
    
    # If editing a student, fetch their details to prefill the form
    if edit_id:
        try:
            edit_student = conn.execute("SELECT * FROM students WHERE id = ?", (int(edit_id),)).fetchone()
        except ValueError:
            pass
            
    # Fetch all student records
    students_rows = conn.execute("SELECT * FROM students ORDER BY id ASC").fetchall()
    
    # Convert SQLite Row objects to list of dicts for Jinja templates
    students = [dict(row) for row in students_rows]
        
    conn.close()
    
    return render_template(
        'index.html', 
        students=students, 
        edit_student=edit_student
    )

@app.route('/add', methods=['POST'])
def add_student():
    """Handles adding a new student to the database."""
    name = request.form.get('name', '').strip()
    age_str = request.form.get('age', '').strip()
    
    if not name or not age_str:
        flash("Name and Age are required fields.", "error")
        return redirect(url_for('index'))
        
    try:
        age = int(age_str)
        if age < 1 or age > 120:
            flash("Age must be between 1 and 120.", "error")
            return redirect(url_for('index'))
    except ValueError:
        flash("Age must be a valid number.", "error")
        return redirect(url_for('index'))
        
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO students (name, age, phone) VALUES (?, ?, ?)",
            (name, age, None)
        )
        conn.commit()
        flash(f"Student '{name}' added successfully!", "success")
    except Exception as e:
        flash(f"Error adding student: {e}", "error")
    finally:
        conn.close()
        
    return redirect(url_for('index'))

@app.route('/edit/<int:student_id>', methods=['POST'])
def edit_student(student_id):
    """Handles updating an existing student's details."""
    name = request.form.get('name', '').strip()
    age_str = request.form.get('age', '').strip()
    
    if not name or not age_str:
        flash("Name and Age are required fields.", "error")
        return redirect(url_for('index', edit=student_id))
        
    try:
        age = int(age_str)
        if age < 1 or age > 120:
            flash("Age must be between 1 and 120.", "error")
            return redirect(url_for('index', edit=student_id))
    except ValueError:
        flash("Age must be a valid number.", "error")
        return redirect(url_for('index', edit=student_id))
        
    conn = get_db_connection()
    try:
        conn.execute(
            "UPDATE students SET name = ?, age = ? WHERE id = ?",
            (name, age, student_id)
        )
        conn.commit()
        flash("Student details updated successfully!", "success")
    except Exception as e:
        flash(f"Error updating student: {e}", "error")
    finally:
        conn.close()
        
    return redirect(url_for('index'))

@app.route('/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    """Deletes a student record from the database."""
    conn = get_db_connection()
    try:
        student = conn.execute("SELECT name FROM students WHERE id = ?", (student_id,)).fetchone()
        if student:
            conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
            conn.commit()
            flash(f"Student '{student['name']}' deleted successfully.", "success")
        else:
            flash("Student record not found.", "error")
    except Exception as e:
        flash(f"Error deleting student: {e}", "error")
    finally:
        conn.close()
        
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)