import boto3
import pymysql
from flask import Flask, request, render_template

# AWS RDS details
region_name = 'ca-central-1'
rds_host = 'database-1.c3yaowwewg7q.ca-central-1.rds.amazonaws.com'
db_username = 'admin'
db_password = '12345678'
db_name = 'student_db_1'

# Flask web application
application = Flask(__name__)

# Render the student data input form
@application.route('/')
def index():
    return render_template('form.html')

# Handle form submission and store data in RDS
@application.route('/submit', methods=['POST'])
def submit():
    # Extract student data from the form
    student_name = request.form['name']
    student_age = request.form['age']
    student_dob = request.form['dob']
    student_address = request.form['address']
    student_city = request.form['city']
    student_grade = request.form['grade']
    parent_name = request.form['parent_name']
    parent_email = request.form['parent_email']
    phone = request.form['phone']
    nationality = request.form['nationality']
    gender = request.form['gender']

    # Connect to the RDS database
    conn = pymysql.connect(host=rds_host, user=db_username, password=db_password, db=db_name, connect_timeout=5)

    try:
        # Create a cursor object
        with conn.cursor() as cursor:
            # Execute SQL query to insert student data into the database
            sql = "INSERT INTO students (name, age, dob, address, city, grade, parent_name, parent_email, phone, nationality, gender) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (student_name, student_age, student_dob, student_address, student_city, student_grade, parent_name, parent_email, phone, nationality, gender))
            # Commit the transaction
            conn.commit()
    finally:
        # Close the connection
        conn.close()

    return """
    <script>
        alert('Data submitted successfully!');
        window.location.href = "/";
    </script>
    """
if __name__ == '__main__':
    application.run(debug=True)
