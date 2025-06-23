# ==================== IMPORTS ====================
from flask import Flask, render_template, request  # Flask for web app, render_template for HTML rendering, request for handling form data
import sqlite3  # For database operations
from datetime import datetime  # For handling date and time


# ==================== FLASK APP INITIALIZATION ====================
app = Flask(__name__)  # Create a Flask application instance


# ==================== DATABASE HELPERS ====================
def get_subjects():
    """
    Retrieve distinct subjects from the database.
    
    Returns:
        list: A list of distinct subject names.
    """
    conn = sqlite3.connect('attendance.db')  # Connect to the SQLite database
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM subjects")  # Fetch distinct subjects
    subjects = [row[0] for row in cursor.fetchall()]  # Extract subject names
    conn.close()  # Close the database connection
    return subjects


def get_attendance(selected_date, selected_subject):
    """
    Retrieve attendance records for a given date and subject.
    
    Args:
        selected_date (str): The date in 'YYYY-MM-DD' format.
        selected_subject (str): The selected subject.
    
    Returns:
        list: A list of tuples containing attendance records (name, time).
    """
    conn = sqlite3.connect('attendance.db')  # Connect to the SQLite database
    cursor = conn.cursor()
    # Fetch attendance records for the given date and subject
    cursor.execute("SELECT name, time FROM attendance WHERE date = ? AND subject = ?", (selected_date, selected_subject))
    attendance_data = cursor.fetchall()  # Get all matching records
    conn.close()  # Close the database connection
    return attendance_data


# ==================== ROUTES ====================
@app.route('/')
def index():
    """
    Render the main page with subject options.
    
    Returns:
        HTML: The rendered index.html template with subject options.
    """
    subjects = get_subjects()  # Get the list of subjects
    return render_template(
        'index.html',
        subjects=subjects,
        selected_date='',
        selected_subject='',
        no_data=False
    )


@app.route('/attendance', methods=['POST'])
def attendance():
    """
    Handle form submission to display attendance records.
    
    Returns:
        HTML: The rendered index.html template with attendance data.
    """
    selected_date = request.form.get('selected_date')  # Get the selected date from the form
    selected_subject = request.form.get('selected_subject')  # Get the selected subject from the form

    # Validate form inputs
    if not selected_date or not selected_subject:
        return render_template(
            'index.html',
            subjects=get_subjects(),
            selected_date=selected_date,
            selected_subject=selected_subject,
            no_data=True  # Show a message like "Please select a date and subject"
        )

    # Fetch attendance data for the selected date and subject
    attendance_data = get_attendance(selected_date, selected_subject)

    # Render the template with attendance data (or no_data message)
    return render_template(
        'index.html',
        subjects=get_subjects(),
        selected_date=selected_date,
        selected_subject=selected_subject,
        attendance_data=attendance_data,
        no_data=not attendance_data  # True if data is empty
    )


# ==================== RUN APP ====================
if __name__ == '__main__':
    # Run the Flask app in debug mode and listen on all interfaces
    app.run(debug=True, host="0.0.0.0", port=5000)
