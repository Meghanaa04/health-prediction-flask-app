from flask import Flask, render_template, request, redirect
import sqlite3
import re
from datetime import datetime

app = Flask(__name__)


# Create Database
def init_db():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            email TEXT NOT NULL,
            glucose REAL NOT NULL,
            haemoglobin REAL NOT NULL,
            cholesterol REAL NOT NULL,
            remarks TEXT
        )
    ''')

    conn.commit()
    conn.close()


init_db()


# Home Page
@app.route('/')
def home():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM patients")
    patients = cursor.fetchall()

    conn.close()

    return render_template(
        'index.html',
        patients=patients
    )


# Add Patient
@app.route('/add', methods=['GET', 'POST'])
def add_patient():

    if request.method == 'POST':

        full_name = request.form['full_name']
        dob = request.form['dob']
        email = request.form['email']
        glucose = request.form['glucose']
        haemoglobin = request.form['haemoglobin']
        cholesterol = request.form['cholesterol']

        # Email Validation
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(email_pattern, email):
            return render_template(
                'error.html',
                message="Invalid Email Address"
            )

        # DOB Validation
        dob_date = datetime.strptime(
            dob,
            "%Y-%m-%d"
        ).date()

        if dob_date > datetime.today().date():
            return render_template(
                'error.html',
                message="Date of Birth cannot be in the future"
            )

        # Negative Values Validation
        if (
            float(glucose) < 0 or
            float(haemoglobin) < 0 or
            float(cholesterol) < 0
        ):
            return render_template(
                'error.html',
                message="Blood values cannot be negative"
            )

        # Prediction Logic
        if float(glucose) > 140:
            remarks = "High Diabetes Risk"

        elif float(haemoglobin) < 12:
            remarks = "Possible Anemia Risk"

        elif float(cholesterol) > 240:
            remarks = "High Cholesterol Risk"

        else:
            remarks = "Healthy Range"

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        cursor.execute(
            '''
            INSERT INTO patients
            (
                full_name,
                dob,
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (
                full_name,
                dob,
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks
            )
        )

        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('add_patient.html')


# Edit Patient
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':

        full_name = request.form['full_name']
        dob = request.form['dob']
        email = request.form['email']
        glucose = request.form['glucose']
        haemoglobin = request.form['haemoglobin']
        cholesterol = request.form['cholesterol']

        # Email Validation
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        if not re.match(email_pattern, email):
            return render_template(
                'error.html',
                message="Invalid Email Address"
            )

        # DOB Validation
        dob_date = datetime.strptime(
            dob,
            "%Y-%m-%d"
        ).date()

        if dob_date > datetime.today().date():
            return render_template(
                'error.html',
                message="Date of Birth cannot be in the future"
            )

        # Negative Values Validation
        if (
            float(glucose) < 0 or
            float(haemoglobin) < 0 or
            float(cholesterol) < 0
        ):
            return render_template(
                'error.html',
                message="Blood values cannot be negative"
            )

        # Prediction Logic
        if float(glucose) > 140:
            remarks = "High Diabetes Risk"

        elif float(haemoglobin) < 12:
            remarks = "Possible Anemia Risk"

        elif float(cholesterol) > 240:
            remarks = "High Cholesterol Risk"

        else:
            remarks = "Healthy Range"

        cursor.execute(
            '''
            UPDATE patients
            SET
                full_name=?,
                dob=?,
                email=?,
                glucose=?,
                haemoglobin=?,
                cholesterol=?,
                remarks=?
            WHERE id=?
            ''',
            (
                full_name,
                dob,
                email,
                glucose,
                haemoglobin,
                cholesterol,
                remarks,
                id
            )
        )

        conn.commit()
        conn.close()

        return redirect('/')

    cursor.execute(
        "SELECT * FROM patients WHERE id=?",
        (id,)
    )

    patient = cursor.fetchone()

    conn.close()

    return render_template(
        'edit_patient.html',
        patient=patient
    )


# Delete Patient
@app.route('/delete/<int:id>')
def delete_patient(id):

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id=?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect('/')


# Reset Database
@app.route('/reset')
def reset_database():

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM patients")
    cursor.execute(
        "DELETE FROM sqlite_sequence WHERE name='patients'"
    )

    conn.commit()
    conn.close()

    return redirect('/')


if __name__ == '__main__':
    app.run(debug=False)