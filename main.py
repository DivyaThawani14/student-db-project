import tkinter as tk
from tkinter import messagebox
import mysql.connector
import re

# Function to validate email format
def validate_email(email):
    # Regular expression for basic email format validation
    pattern = r'^[a-zA-Z][a-zA-Z0-9._]*@[a-zA-Z]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email)

# Function to validate age format
def validate_age(age):
    return age.isdigit()

# Function to handle form submission
def submit_form():
    # Retrieve data from form fields
    name = entry_name.get()
    email = entry_email.get()
    age = entry_age.get()
    gender = var_gender.get()  # Get selected gender from dropdown
    address = entry_address.get()
    city = entry_city.get()
    state = var_state.get()  # Get selected state from dropdown
    country = var_country.get()  # Get selected country from dropdown

    # Perform basic data validation
    if not name or not email or not age or not gender or not address or not city or not state or not country:
        messagebox.showerror("Error", "Please fill in all fields")
        return

    if not validate_email(email):
        messagebox.showerror("Error", "Invalid email format")
        return

    if not validate_age(age):
        messagebox.showerror("Error", "Age must be a valid integer")
        return

    try:
        # Connect to the MySQL database
        cnx = mysql.connector.connect(
            host='database-1.cp4iuymugi65.eu-central-1.rds.amazonaws.com',
            user='admin',
            password='admin123',
            database='database-1>'
        )
        
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

        # Show success message
        messagebox.showinfo("Success", "Data submitted successfully")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

# Create main application window
root = tk.Tk()
root.title("Student Information Form")

# Create form elements with improved design and spacing
label_name = tk.Label(root, text="Name:")
label_name.grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(root)
entry_name.grid(row=0, column=1, padx=10, pady=5)

label_email = tk.Label(root, text="Email:")
label_email.grid(row=1, column=0, padx=10, pady=5)
entry_email = tk.Entry(root)
entry_email.grid(row=1, column=1, padx=10, pady=5)

label_age = tk.Label(root, text="Age:")
label_age.grid(row=2, column=0, padx=10, pady=5)
entry_age = tk.Entry(root)
entry_age.grid(row=2, column=1, padx=10, pady=5)

label_gender = tk.Label(root, text="Gender:")
label_gender.grid(row=3, column=0, padx=10, pady=5)
gender_options = ["Male", "Female", "Both"]  # Options for gender dropdown
var_gender = tk.StringVar(root)  # Variable to store selected gender
var_gender.set(gender_options[0])  # Set default value
gender_dropdown = tk.OptionMenu(root, var_gender, *gender_options)
gender_dropdown.grid(row=3, column=1, padx=10, pady=5)

label_address = tk.Label(root, text="Address:")
label_address.grid(row=4, column=0, padx=10, pady=5)
entry_address = tk.Entry(root)
entry_address.grid(row=4, column=1, padx=10, pady=5)

label_city = tk.Label(root, text="City:")
label_city.grid(row=5, column=0, padx=10, pady=5)
entry_city = tk.Entry(root)
entry_city.grid(row=5, column=1, padx=10, pady=5)

label_state = tk.Label(root, text="State:")
label_state.grid(row=6, column=0, padx=10, pady=5)
state_options = ["New York", "California", "Texas", "Florida", "Ohio"]  # Options for state dropdown
var_state = tk.StringVar(root)  # Variable to store selected state
var_state.set(state_options[0])  # Set default value
state_dropdown = tk.OptionMenu(root, var_state, *state_options)
state_dropdown.grid(row=6, column=1, padx=10, pady=5)

label_country = tk.Label(root, text="Country:")
label_country.grid(row=7, column=0, padx=10, pady=5)
country_options = ["USA", "Canada", "UK", "Australia", "India"]  # Options for country dropdown
var_country = tk.StringVar(root)  # Variable to store selected country
var_country.set(country_options[0])  # Set default value
country_dropdown = tk.OptionMenu(root, var_country, *country_options)
country_dropdown.grid(row=7, column=1, padx=10, pady=5)

submit_button = tk.Button(root, text="Submit", command=submit_form)
submit_button.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

# Start the application
root.mainloop()
