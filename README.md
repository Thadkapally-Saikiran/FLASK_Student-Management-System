# 🚀 Student Management System (SMS) 🚀

## Overview

This is a **Student Management System (SMS)** built as part of my full-stack development training. The application is designed to manage student records with user authentication, allowing users to register, login, view, add, edit, and delete student data. The system uses **Flask** for the backend, **MySQL** for database management, and **Bootstrap** for the frontend styling.

## Key Features

### 🔑 User Authentication:
- Registration, Login, and Logout functionality.
- Secure user management with session handling.

### 📚 Student Management:
- Register new students with fields such as Name, Address, Age, and Email.
- View and manage student data in a structured table.
- Edit student records to keep data up-to-date.
- Delete student records with a confirmation process.

### 📊 Data Export:
- Ability to export student data to Excel for easy download.

## 💻 Technologies Used
- 🟢 **Backend**: Python, Flask, MySQL
- 🟢 **Frontend**: HTML, CSS, Bootstrap
- 🟢 **Database**: MySQL
- 🟢 **Other**: Jinja2 templates for dynamic HTML rendering, Flash messaging for user notifications.

## Project Highlights:
- Integrated Flask with MySQL to build a fully functional application for managing student data.
- CRUD operations (Create, Read, Update, Delete) implemented to manage student records effectively.
- Designed a user-friendly interface with Bootstrap to ensure a seamless experience for both students and admins.
- Ensured security and smooth functionality through the use of sessions and authentication.

## 💡 Learning Outcomes:
This project has allowed me to enhance my skills in web development, **Python** programming, and **database management**. It’s been a great journey from learning **Flask** concepts to implementing them in a fully operational system.

## Steps to Set Up and Run the Project

### 1. Create a Virtual Environment
First, create a new directory for your project and navigate to it in your terminal or command prompt:

```
mkdir sms_project
cd sms_project
```


### Now, create a virtual environment:
```
python -m venv venv
```

### 2. Activate the Virtual Environment
On Windows:
```
venv\Scripts\activate
```
### 3. Install the Required Packages
Inside the virtual environment, install Flask and MySQL connector:
```
pip install flask mysql-connector-python pandas
```

### 4. Create the Project Structure
Inside the sms_project folder, create the following structure:
```
sms_project/
├── venv/             # Virtual Environment
├── app.py            # Main Flask app
└── templates/        # HTML Templates folder
    ├── homepage.html
    ├── register.html
    ├── login.html
    ├── student_register.html
    ├── student_list.html
    ├── editstudent.html
    ├── delete_confirmation.html
    └── nav.html      # Navigation bar template
```

### 5. Add the Code Files
- Copy the Flask app code (app.py) and your HTML templates into the appropriate files and directories.
- In app.py, ensure to set up the Flask routes, database connections, and form handling (refer to the previously shared app.py code).

### 6. Set Up MySQL Database
- Create a new MySQL database called sms.
- Set up the necessary tables for signup and students.

### 7. Run the Flask Application
In the project folder, run the following command:
```
python app.py
```
Flask will start the development server, and you will see an output like this:
```
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
### 8. Access the Application in Your Browser
Open a web browser and go to:
```
http://127.0.0.1:5000/
```



