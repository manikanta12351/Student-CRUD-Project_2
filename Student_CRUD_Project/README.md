# Student CRUD Project

A sleek and responsive single-page web application for managing student records (Create, Read, Update, Delete) built with Python, Flask, SQLite, and vanilla CSS.

## Features

- **Add Students**: Register new student records with name, age, and phone.
- **View Students**: See a list of all registered student records in a clean tabular view.
- **Edit Students**: Update student records inline or using forms.
- **Delete Students**: Remove student records safely from the database.
- **Database Persistence**: SQLite database setup with automatic schema initialization.

## Technology Stack

- **Backend**: Python (Flask, SQLite3)
- **Frontend**: HTML5, Vanilla CSS, Jinja2 Templates

## Project Structure

```text
Student_CRUD_Project/
│
├── app.py                # Main Flask application and database routing
├── students.db           # SQLite database storing student records
├── static/
│   └── style.css         # Styling for the application
└── templates/
    ├── index.html        # Main single-page list and form view
    └── edit.html         # Edit page template
```

## Setup and Running Instructions

1. **Clone or navigate to the project directory:**
   ```bash
   cd Student_CRUD_Project
   ```

2. **Install Flask:**
   Make sure you have Python installed, then install Flask using pip:
   ```bash
   pip install Flask
   ```

3. **Run the Application:**
   Start the local Flask development server:
   ```bash
   python app.py
   ```

4. **Access the Web App:**
   Open your browser and navigate to:
   ```text
   http://127.0.0.1:5000
   ```
