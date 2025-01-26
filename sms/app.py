# Importing required libraries
from flask import Flask, send_file, session, flash, jsonify, render_template, request, redirect, url_for
import pandas as pd  # Pandas library for data manipulation and Excel handling
import os  # To interact with the operating system, e.g., file handling
import mysql.connector  # MySQL connector for database interaction
from mysql.connector import Error  # For handling MySQL errors

# Create a Flask application instance
app = Flask(__name__)

# Setting a secret key for sessions (needed for secure sessions in Flask)
app.secret_key = 'mysecretkeyistopersonal'  # Secret key for securing user sessions

# Connection helper function to connect to the database
def get_db_connection():
    try:
        # Establishing the connection to the MySQL database
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='SaiKiran@2001',
            db='sms'
        )
        return mydb  # Return the database connection object if successful
    except Error as e:
        print(f"Database connection error: {e}")  # Error handling if connection fails
        return None  # Return None if connection failed

# Route to show a user's profile (example route)
@app.route('/user/<username>')
def show_user_profile(username):
    return f'User {username}'  # Simple route returning the username passed in the URL

# Route with an integer parameter to show whether a number is less than 25
@app.route('/allow/<int:Number>')
def allow(Number):
    if Number < 25:  # Check if the passed number is less than 25
        return f'You have been allowed to enter because your number is {str(Number)}'
    else:
        return f'You are not allowed'  # Return if number is greater than or equal to 25

# Route using UUID to fetch user details by ID
@app.route('/useruid/<uuid:user_id>', methods=['GET'])
def get_user_by_uuid(user_id):
    return f'user_id: {str(user_id)}'  # Returning user ID from URL parameter

# Another route using UUID to return JSON data
@app.route('/manuid/<uuid:man_id>', methods=['GET'])
def get_man_by_uuid(man_id):
    return jsonify({
        'message': 'User fetched successfully',  # Return success message
        'user_id': str(man_id)  # Return the user ID as part of the JSON response
    })

# Route to return a file path for files
@app.route('/files/<path:file_path>', methods=['GET'])
def get_file_by_path(file_path):
    return jsonify({
        "message": "File path processed successfully",  # Success message
        "file_path": file_path  # Return the file path as part of the JSON response
    })

# Homepage route that renders 'homepage.html'
@app.route('/')
def homepage():
    return render_template('homepage.html')  # Renders the homepage template

# Route for user registration, handles both GET and POST methods
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":  # If the request is POST (form submission)
        # Extracting form data
        username = request.form['username']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        password = request.form['password']
        print(username, mobile, email, address, password)

        mydb = get_db_connection()  # Getting the DB connection
        if mydb:  # If DB connection is successful
            cursor = mydb.cursor()
            cursor.execute('INSERT INTO signup VALUES (%s, %s, %s, %s, %s)', [username, mobile, email, address, password])  # Insert user data into the 'signup' table
            mydb.commit()  # Committing changes to the database
            cursor.close()  # Closing cursor
            print('Details registered')
    return render_template('register.html')  # Rendering the registration page template

# Login route that handles both GET and POST methods
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # If the request is POST (form submission)
        # Extracting form data
        email = request.form['email']
        password = request.form['password']

        mydb = get_db_connection()  # Getting the DB connection
        if mydb:  # If DB connection is successful
            cursor = mydb.cursor()
            cursor.execute('SELECT COUNT(*) FROM signup WHERE email=%s AND password=%s', [email, password])  # Querying the database to check user credentials
            count = cursor.fetchone()[0]  # Fetching the count (1 if the user exists, 0 if not)
            cursor.close()  # Closing the cursor
            mydb.close()  # Closing the database connection
            print(count)

            if count == 0:  # If no matching user found
                return render_template('login.html')  # Re-render the login page
            else:  # If user found
                session['user'] = request.form.get('email')  # Storing email in session to keep the user logged in
                print(session)
                flash('Login Successful', 'success')  # Flash message indicating successful login
                return redirect(url_for('student_register'))  # Redirecting to the student registration page
    return render_template('login.html')  # Rendering the login page template

# Student registration route that handles both GET and POST methods
@app.route('/std_reg', methods=['GET', 'POST'])
def student_register():
    if 'user' in session:  # Check if the user is logged in (i.e., 'user' key exists in session)
        if request.method == 'POST':  # If the request is POST (form submission)
            # Extracting student registration form data
            name = request.form['name']
            address = request.form['Address']
            age = request.form['age']
            email = request.form['email']

            mydb = get_db_connection()  # Getting the DB connection
            if mydb:  # If DB connection is successful
                cursor = mydb.cursor()
                cursor.execute("INSERT INTO students (name, address, age, email) VALUES (%s, %s, %s, %s)", (name, address, age, email))  # Inserting student data into the 'students' table
                mydb.commit()  # Committing changes to the database
                cursor.close()  # Closing the cursor
                mydb.close()  # Closing the DB connection
                flash("Student registered successfully!", "success")  # Flash message for successful registration
            return redirect(url_for('student_list'))  # Redirecting to the student list page after successful registration
    else:
        return redirect(url_for('login'))  # Redirecting to the login page if the user is not logged in
    return render_template('student_register.html')  # Rendering the student registration page template

# Route to display the list of students
@app.route('/student_list')
def student_list():
    if 'user' in session:  # If the user is logged in
        mydb = get_db_connection()  # Getting the DB connection
        if mydb:  # If DB connection is successful
            cursor = mydb.cursor(dictionary=True)
            cursor.execute("SELECT * FROM students")  # Querying all student data from the 'students' table
            students = cursor.fetchall()  # Fetching all results
            cursor.close()  # Closing the cursor
            mydb.close()  # Closing the DB connection
            print(students)
            return render_template('student_list.html', students=students)  # Rendering the student list page and passing the student data
        flash("Unable to connect to the database.", "error")  # Flash message if DB connection fails
    else:
        return redirect(url_for('login'))  # Redirect to login if the user is not logged in
    return render_template('student_list.html', students=[])  # Rendering the student list page with an empty list

# Route to edit student details
@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    mydb = get_db_connection()  # Getting the DB connection
    if mydb:  # If DB connection is successful
        cursor = mydb.cursor(dictionary=True)
        cursor.execute('SELECT * FROM students WHERE id=%s', (id,))  # Querying student data by ID
        student = cursor.fetchone()  # Fetching the student data
        if request.method == 'POST':  # If the request is POST (form submission)
            # Extracting the updated student data
            name = request.form['name']
            address = request.form['Address']
            age = request.form['age']
            email = request.form['email']
            cursor.execute(
                "UPDATE students SET name=%s, address=%s, age=%s, email=%s WHERE id=%s", (name, address, age, email, id)
            )  # Updating the student data in the database
            mydb.commit()  # Committing changes to the database
            flash("Student details updated successfully!", "success")  # Flash message indicating success
        cursor.close()  # Closing the cursor
        mydb.close()  # Closing the DB connection
        return render_template('editstudent.html', student=student)  # Rendering the student edit page with the current student data
    flash("Unable to connect to the database.", "error")  # Flash message if DB connection fails
    return redirect(url_for('student_list'))  # Redirecting to the student list page if DB connection fails

# Route to delete a student
@app.route('/delete_student/<int:id>', methods=['GET', 'POST'])
def delete_student(id):
    if request.method == "POST":  # If the request is POST (confirmation of deletion)
        mydb = get_db_connection()  # Getting the DB connection
        cursor = mydb.cursor()
        cursor.execute("DELETE FROM students WHERE id=%s", (id,))  # Deleting the student from the database
        mydb.commit()  # Committing changes to the database
        mydb.close()  # Closing the DB connection
        flash("Student deleted successfully", "success")  # Flash message indicating successful deletion
        return redirect(url_for('student_list'))  # Redirecting to the student list page after deletion
    mydb = get_db_connection()  # Getting the DB connection
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))  # Querying student data by ID
    student = cursor.fetchone()  # Fetching the student data
    mydb.close()  # Closing the DB connection
    return render_template('Delete_confirmation.html', student=student)  # Rendering the delete confirmation page

# Route to download the student data as an Excel file
@app.route('/download_excel')
def download_excel():
    mydb = get_db_connection()  # Getting the DB connection
    if mydb:  # If DB connection is successful
        cursor = mydb.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students")  # Querying all student data from the 'students' table
        students = cursor.fetchall()  # Fetching all results
        df = pd.DataFrame(students)  # Converting student data to a pandas DataFrame
        file_path = 'students_data.xlsx'  # File path for saving the Excel file
        df.to_excel(file_path, index=False)  # Saving the student data to an Excel file
        cursor.close()  # Closing the cursor
        mydb.close()  # Closing the DB connection
        return send_file(file_path, as_attachment=True)  # Sending the file as an attachment to the client
    flash("Unable to connect to the database.", "error")  # Flash message if DB connection fails
    return redirect(url_for('student_list'))  # Redirecting to the student list page if DB connection fails

# Route to log the user out
@app.route('/logout')
def logout():
    session.pop('user', None)  # Removing the 'user' key from the session to log the user out
    flash("You have been logged out.", "info")  # Flash message indicating successful logout
    return redirect(url_for('homepage'))  # Redirecting to the login page after logout

# Running the application on the specified host and port
if __name__ == '__main__':
    app.run(debug=True)
