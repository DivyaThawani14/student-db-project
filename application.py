from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
import re

application = Flask(__name__)
application.secret_key = 'divya'  # Change this to your secret key

# Function to validate email format
def validate_email(email):
    # Regular expression for basic email format validation
    pattern = r'^[a-zA-Z][a-zA-Z0-9._]*@[a-zA-Z]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Function to validate age format
def validate_age(age):
    return age.isdigit()

# Function to connect to the MySQL database
def connect_db():
    return mysql.connector.connect(
        host='database-1.cpo8g8224nk4.us-west-2.rds.amazonaws.com',
        user='admin',
        password='admin123',
        database='database_rds'
    )

# Route for the form page
application = Flask(__name__)

# Route to handle form submission
@application.route('/submit_form', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Retrieve data from form fields
        name = request.form['name']
        email = request.form['email']
        age = request.form['age']
        gender = request.form['gender']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']

        # Perform basic data validation
        if not name or not email or not age or not gender or not address or not city or not state or not country:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('index'))

        if not validate_email(email):
            flash('Invalid email format', 'error')
            return redirect(url_for('index'))

        if not validate_age(age):
            flash('Age must be a valid integer', 'error')
            return redirect(url_for('index'))

        try:
            # Connect to the MySQL database
            cnx = connect_db()
            
            # Create a cursor object
            cursor = cnx.cursor()

            # Define the SQL query to insert data into the table
            sql = "INSERT INTO students_data (name, email, age, gender, address, city, state, country) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

            # Execute the SQL query with user input as parameters
            cursor.execute(sql, (name, email, age, gender, address, city, state, country))

            # Commit the transaction
            cnx.commit()

            # Close the cursor and connection
            cursor.close()
            cnx.close()

            flash('Data submitted successfully', 'success')
            return redirect(url_for('index'))
        except mysql.connector.Error as err:
            flash(f'Error: {err}', 'error')
            return redirect(url_for('index'))

if __name__ == '__main__':
    application.run(debug=True)
