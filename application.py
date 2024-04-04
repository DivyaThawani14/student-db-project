from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import re

# Create Flask application instance
application = Flask(__name__)
application.secret_key = 'your_secret_key'  # Change this to a secure secret key

# Function to validate email format
def validate_email(email):
    pattern = r'^[a-zA-Z][a-zA-Z0-9._]*@[a-zA-Z]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Function to validate age format
def validate_age(age):
    return age.isdigit()

# Function to connect to the MySQL database
def connect_db():
    try:
        cnx = mysql.connector.connect(
            host='database-1.cpo8g8224nk4.us-west-2.rds.amazonaws.com',
            user='admin',
            password='admin123',
            database='database_rds'
        )
        return cnx
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

# Route for the form page
@application.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@application.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']

        if not all([name, email, age, gender, address, city, state, country]):
            flash('Please fill in all fields', 'error')
            return redirect(url_for('index'))

        if not validate_email(email):
            flash('Invalid email format', 'error')
            return redirect(url_for('index'))

        if not validate_age(age):
            flash('Age must be a valid integer', 'error')
            return redirect(url_for('index'))

        try:
            cnx = connect_db()
            if cnx:
                cursor = cnx.cursor()

                sql = "INSERT INTO students_data (name, email, age, gender, address, city, state, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, email, age, gender, address, city, state, country))

                cnx.commit()

                cursor.close()
                cnx.close()

                flash('Data submitted successfully', 'success')
                return redirect(url_for('index'))
            else:
                flash('Error connecting to the database', 'error')
                return redirect(url_for('index'))
        except mysql.connector.Error as err:
            flash(f'Database error: {err}', 'error')
            return redirect(url_for('index'))

if __name__ == '__main__':
    application.run(debug=True)

