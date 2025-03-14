# =============================================================================
# IMPORTS AND APP CONFIGURATION
# =============================================================================
from flask import Flask, send_file, session, flash, jsonify, render_template, request, redirect, url_for  # Import Flask and related functions for web handling, sessions, flashing messages, etc.
import pandas as pd  # Import pandas for data manipulation and Excel file creation
import os  # Import os module for operating system related functions
import mysql.connector  # Import mysql.connector to connect and interact with MySQL databases
from mysql.connector import Error  # Import Error class from mysql.connector for error handling

app = Flask(__name__)  # Create a new Flask web application instance
app.secret_key = 'mysecretkeyistopersonal'  # Set the secret key used for securing sessions

# =============================================================================
# DATABASE CONNECTION HELPER
# =============================================================================
def get_db_connection():
    # Try to establish a connection to the MySQL database
    try:
        mydb = mysql.connector.connect(
            host='localhost',         # Database host
            user='root',              # Database username
            password='SaiKiran@2001',  # Database password
            db='sms'                  # Database name (sms)
        )
        return mydb  # Return the database connection object if successful
    except Error as e:
        print(f"Database connection error: {e}")  # Print error message if connection fails
        return None  # Return None if unable to connect

# =============================================================================
# SIMPLE DEMO ROUTES
# =============================================================================

@app.route('/user/<username>')  # Define a route that accepts a username as a URL parameter
def show_user_profile(username):
    return f'User {username}'  # Return a simple string displaying the username

@app.route('/allow/<int:Number>')  # Define a route that accepts an integer parameter 'Number'
def allow(Number):
    if Number < 25:  # Check if the provided number is less than 25
        return f'You have been allowed to enter because your number is {str(Number)}'  # Return an allowed message with the number
    else:
        return 'You are not allowed'  # Return a not allowed message if number is 25 or greater

@app.route('/useruid/<uuid:user_id>', methods=['GET'])  # Define a route that accepts a UUID parameter using GET method
def get_user_by_uuid(user_id):
    return f'user_id: {str(user_id)}'  # Return the string representation of the UUID

@app.route('/manuid/<uuid:man_id>', methods=['GET'])  # Define a route that accepts a UUID parameter for "man_id" using GET method
def get_man_by_uuid(man_id):
    return jsonify({
        'message': 'User fetched successfully',  # Return a success message
        'user_id': str(man_id)                   # Return the string version of the UUID
    })  # Respond with JSON data

@app.route('/files/<path:file_path>', methods=['GET'])  # Define a route to accept a file path as a parameter
def get_file_by_path(file_path):
    return jsonify({
        "message": "File path processed successfully",  # Success message
        "file_path": file_path                           # Return the received file path
    })  # Respond with JSON data

# =============================================================================
# HOMEPAGE ROUTE
# =============================================================================
@app.route('/')  # Define the route for the homepage
def homepage():
    return render_template('homepage.html')  # Render and return the homepage template

# =============================================================================
# USER REGISTRATION ROUTE
# =============================================================================
@app.route('/register', methods=['GET', 'POST'])  # Define a route for user registration that supports GET and POST methods
def register():
    if request.method == "POST":  # Check if the request method is POST (i.e., form submission)
        username = request.form['username']  # Retrieve 'username' from the submitted form data
        mobile = request.form['mobile']      # Retrieve 'mobile' from the form data
        email = request.form['email']        # Retrieve 'email' from the form data
        address = request.form['address']    # Retrieve 'address' from the form data
        password = request.form['password']  # Retrieve 'password' from the form data
        print(username, mobile, email, address, password)  # Print the registration details for debugging

        mydb = get_db_connection()  # Get a database connection
        if mydb:  # If the connection is successful
            cursor = mydb.cursor()  # Create a cursor object to execute SQL queries
            cursor.execute(
                'INSERT INTO signup VALUES (%s, %s, %s, %s, %s)',  # SQL query to insert a new record into the signup table
                [username, mobile, email, address, password]  # Data to be inserted
            )
            mydb.commit()  # Commit the transaction to save the changes
            cursor.close()  # Close the cursor
            flash("Registration successful! Please login.", "success")  # Flash a success message to the user
            return redirect(url_for('login'))  # Redirect the user to the login page after successful registration
        else:
            flash("Unable to connect to the database.", "error")  # Flash an error message if connection failed
    return render_template('register.html')  # Render and return the registration template for GET requests or on error

# =============================================================================
# USER LOGIN ROUTE
# =============================================================================
@app.route('/login', methods=['GET', 'POST'])  # Define a route for user login supporting GET and POST methods
def login():
    if request.method == 'POST':  # Check if the request method is POST (form submission)
        email = request.form['email']  # Retrieve the email from the login form
        password = request.form['password']  # Retrieve the password from the login form

        mydb = get_db_connection()  # Get a database connection
        if mydb:  # If connection is successful
            cursor = mydb.cursor()  # Create a cursor object
            cursor.execute(
                'SELECT COUNT(*) FROM signup WHERE email=%s AND password=%s',  # SQL query to check if a matching user exists
                [email, password]  # Parameters for the query
            )
            count = cursor.fetchone()[0]  # Fetch the count result from the query
            cursor.close()  # Close the cursor
            mydb.close()  # Close the database connection

            if count == 0:  # If no matching user is found
                flash("Invalid credentials. Please try again.", "error")  # Flash an error message
                return render_template('login.html')  # Re-render the login page for another attempt
            else:  # If a matching user is found
                session['user'] = email  # Store the user's email in the session to mark them as logged in
                flash("Login successful", "success")  # Flash a success message

                # After logging in, check if there is a 'next' URL stored in session
                next_page = session.pop('next', None)  # Retrieve and remove 'next' from the session if it exists
                if next_page:
                    return redirect(next_page)  # Redirect to the originally requested page
                else:
                    return redirect(url_for('student_register'))  # Otherwise, redirect to the student registration page
        else:
            flash("Unable to connect to the database.", "error")  # Flash an error if the database connection fails
    return render_template('login.html')  # Render and return the login template for GET requests

# =============================================================================
# STUDENT REGISTRATION ROUTE
# =============================================================================
@app.route('/std_reg', methods=['GET', 'POST'])  # Define a route for student registration that supports GET and POST methods
def student_register():
    if 'user' not in session:  # Check if the user is not logged in
        session['next'] = request.url  # Store the current URL in session so user can be redirected back after login
        flash("Please log in to register students.", "error")  # Flash an error message indicating login is required
        return redirect(url_for('login'))  # Redirect the user to the login page
    elif 'user' in session:  # If the user is logged in
        if request.method == 'POST':  # Check if the request method is POST (form submission)
            name = request.form['name']  # Retrieve the student's name from the form
            address = request.form['Address']  # Retrieve the student's address from the form (note the capital 'A')
            age = request.form['age']  # Retrieve the student's age from the form
            email = request.form['email']  # Retrieve the student's email from the form

            mydb = get_db_connection()  # Get a database connection
            if mydb:  # If connection is successful
                cursor = mydb.cursor()  # Create a cursor object
                cursor.execute(
                    "INSERT INTO students (name, address, age, email) VALUES (%s, %s, %s, %s)",  # SQL query to insert a new student
                    (name, address, age, email)  # Data values for the query
                )
                mydb.commit()  # Commit the transaction
                cursor.close()  # Close the cursor
                mydb.close()  # Close the database connection
                flash("Student registered successfully!", "success")  # Flash a success message
                return redirect(url_for('student_list'))  # Redirect to the student list page
            else:
                flash("Unable to connect to the database.", "error")  # Flash an error message if connection fails
        return render_template('student_register.html')  # Render the student registration template for GET requests or errors
    else:
        return redirect(url_for('login'))  # Fallback: redirect to login if user session is somehow not present

# =============================================================================
# STUDENT LIST ROUTE
# =============================================================================
@app.route('/student_list')  # Define a route for viewing the list of students
def student_list():
    if 'user' not in session:  # Check if the user is not logged in
        session['next'] = request.url  # Store the current URL in session to redirect after login
        flash("Please log in to view the student list.", "error")  # Flash an error message indicating login is required
        return redirect(url_for('login'))  # Redirect the user to the login page

    # If the user is logged in, proceed to fetch and display the student list
    mydb = get_db_connection()  # Get a database connection
    if mydb:  # If connection is successful
        cursor = mydb.cursor(dictionary=True)  # Create a cursor that returns dictionary results
        cursor.execute("SELECT * FROM students")  # Execute SQL query to select all students
        students = cursor.fetchall()  # Fetch all student records
        cursor.close()  # Close the cursor
        mydb.close()  # Close the database connection
        return render_template('student_list.html', students=students)  # Render the student list template with the student data
    else:
        flash("Unable to connect to the database.", "error")  # Flash an error message if connection fails
        return render_template('student_list.html', students=[])  # Render the template with an empty student list

# =============================================================================
# STUDENT EDIT ROUTE
# =============================================================================
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])  # Define a route for editing a student, accepting the student's id as an integer parameter
def edit_student(id):
    mydb = get_db_connection()  # Get a database connection
    if mydb:  # If connection is successful
        cursor = mydb.cursor(dictionary=True)  # Create a cursor that returns results as dictionaries
        cursor.execute('SELECT * FROM students WHERE id=%s', (id,))  # Execute SQL query to select the student with the given id
        student = cursor.fetchone()  # Fetch the student record
        if request.method == 'POST':  # If the request method is POST (form submission)
            name = request.form['name']  # Retrieve the updated name from the form
            address = request.form['Address']  # Retrieve the updated address from the form
            age = request.form['age']  # Retrieve the updated age from the form
            email = request.form['email']  # Retrieve the updated email from the form
            cursor.execute(
                "UPDATE students SET name=%s, address=%s, age=%s, email=%s WHERE id=%s",  # SQL query to update student details
                (name, address, age, email, id)  # Data values for the update query
            )
            mydb.commit()  # Commit the transaction
            flash("Student details updated successfully!", "success")  # Flash a success message
            cursor.close()  # Close the cursor
            mydb.close()  # Close the database connection
            return redirect(url_for('student_list'))  # Redirect to the student list page after successful update
        cursor.close()  # Close the cursor if GET request
        mydb.close()  # Close the database connection
        return render_template('editstudent.html', student=student)  # Render the student edit template with the student's current data
    flash("Unable to connect to the database.", "error")  # Flash an error message if unable to connect
    return redirect(url_for('student_list'))  # Redirect to the student list page

# =============================================================================
# STUDENT DELETE ROUTE
# =============================================================================
@app.route('/delete_student/<int:id>', methods=['GET', 'POST'])  # Define a route for deleting a student, accepting the student's id as an integer parameter
def delete_student(id):
    mydb = get_db_connection()  # Get a database connection
    if mydb:  # If connection is successful
        if request.method == "POST":  # If the request method is POST (confirmation of deletion)
            cursor = mydb.cursor()  # Create a cursor object
            cursor.execute("DELETE FROM students WHERE id=%s", (id,))  # Execute SQL query to delete the student with the given id
            mydb.commit()  # Commit the transaction
            cursor.close()  # Close the cursor
            mydb.close()  # Close the database connection
            flash("Student deleted successfully", "success")  # Flash a success message
            return redirect(url_for('student_list'))  # Redirect to the student list page after deletion
        else:  # If the request method is GET (i.e., user is confirming deletion)
            cursor = mydb.cursor(dictionary=True)  # Create a cursor that returns dictionary results
            cursor.execute("SELECT * FROM students WHERE id=%s", (id,))  # Execute SQL query to fetch the student's details
            student = cursor.fetchone()  # Fetch the student record
            cursor.close()  # Close the cursor
            mydb.close()  # Close the database connection
            return render_template('Delete_confirmation.html', student=student)  # Render the deletion confirmation template with the student's data
    flash("Unable to connect to the database.", "error")  # Flash an error message if connection fails
    return redirect(url_for('student_list'))  # Redirect to the student list page

# =============================================================================
# DOWNLOAD EXCEL ROUTE
# =============================================================================
@app.route('/download_excel')  # Define a route for downloading student data as an Excel file
def download_excel():
    mydb = get_db_connection()  # Get a database connection
    if mydb:  # If connection is successful
        cursor = mydb.cursor(dictionary=True)  # Create a cursor that returns dictionary results
        cursor.execute("SELECT * FROM students")  # Execute SQL query to select all students
        students = cursor.fetchall()  # Fetch all student records
        df = pd.DataFrame(students)  # Convert the list of student dictionaries into a pandas DataFrame
        file_path = 'students_data.xlsx'  # Define the file path for the Excel file
        df.to_excel(file_path, index=False)  # Write the DataFrame to an Excel file without the index
        cursor.close()  # Close the cursor
        mydb.close()  # Close the database connection
        return send_file(file_path, as_attachment=True)  # Send the Excel file to the client as an attachment
    flash("Unable to connect to the database.", "error")  # Flash an error message if connection fails
    return redirect(url_for('student_list'))  # Redirect to the student list page

# =============================================================================
# USER LOGOUT ROUTE
# =============================================================================
@app.route('/logout')  # Define a route for logging out the user
def logout():
    session.pop('user', None)  # Remove the 'user' entry from the session to log the user out
    flash("You have been logged out.", "info")  # Flash an informational message about logout
    return redirect(url_for('homepage'))  # Redirect the user to the homepage

# =============================================================================
# RUN THE APPLICATION
# =============================================================================
if __name__ == '__main__':  # Check if this script is being run directly (and not imported)
    app.run(debug=True)  # Run the Flask app in debug mode, which provides detailed error messages and auto-reload
