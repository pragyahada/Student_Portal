<<<<<<< HEAD
=======
#student fees managment
>>>>>>> 858617f52d7b293272fd561c17641053a5e482c5
🎓 Student Management & Accounting System (Flask)

A Flask-based web application designed to manage students, courses, fees, deposits, admins, and accountants with role-based access control.
The system supports Admin, Accountant, and Student roles with separate dashboards and permissions.

🚀 Features
🔐 Authentication & Authorization

Login & Logout system

Session-based authentication

Role-based access (Admin / Accountant / Student)

Change password for all roles

Unauthorized access handling

👤 User Roles & Capabilities
🛠 Admin

Admin registration & profile management

Upload / change admin profile photo

Register & manage accountants

Register & manage students

Add, edit, and delete courses

View all students, courses, and transactions

Deposit fee payments

View student profiles with fee summary

💼 Accountant

Accountant registration (by admin)

View & manage students

Add courses for students

Collect fee deposits

View transactions

View student fee status

🎓 Student

View personal profile

View enrolled courses

View fee payments & pending dues

Change password

💰 Fee & Course Management

Add courses per student

Course-wise fee tracking

Deposit transactions

Automatic calculation of:

Total fees

Paid amount

Pending dues

Transaction history

📸 Image Upload

Secure admin profile photo upload

Stored in /static/images

Uses werkzeug.utils.secure_filename

🧰 Tech Stack

Backend: Python, Flask

Database: MySQL (PyMySQL)

Frontend: HTML, CSS, Jinja2

File Uploads: Werkzeug

Session Management: Flask Sessions

📁 Project Structure
<<<<<<< HEAD
```
=======
>>>>>>> 858617f52d7b293272fd561c17641053a5e482c5
project/
│
├── app.py
├── mylib.py
├── static/
│   └── images/
├── templates/
│   ├── *.html
│
└── README.md
<<<<<<< HEAD
```

⚙️ Installation & Setup
```
1️⃣ Clone the Repository
git clone https://github.com/your-username/student-management-flask.git
cd student-management-flask
```

2️⃣ Create Virtual Environment (Optional)
```
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```
3️⃣ Install Dependencies
```
=======

⚙️ Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/your-username/student-management-flask.git
cd student-management-flask

2️⃣ Create Virtual Environment (Optional)
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

3️⃣ Install Dependencies
>>>>>>> 858617f52d7b293272fd561c17641053a5e482c5
pip install flask pymysql werkzeug

🗄 Database Setup

Create a MySQL database and required tables:

Required Tables

logindata

admindata

accountantdata

studentdata

coursedata

transactiondata

photodata

Configure database connection inside mylib.py.
<<<<<<< HEAD
```
▶️ Run the Application
```
python app.py
```
=======

▶️ Run the Application
python app.py

>>>>>>> 858617f52d7b293272fd561c17641053a5e482c5

Open browser and visit:

http://127.0.0.1:5000/

🔑 Default Login Flow
Role	Access
Admin	Full system control
Accountant	Student & fee management
Student	Profile & fee details
⚠️ Security Notes

⚠️ Some SQL queries use string concatenation.

Recommended Improvements:

Use parameterized queries everywhere

Hash passwords using werkzeug.security

Enable CSRF protection

Validate file upload types

Add pagination for large tables

Use Flask Blueprints for modular structure

📌 Future Enhancements

Email notifications for fee deposits

Role-based dashboard analytics

Export reports (PDF / Excel)

REST API integration

Attendance module

Online payment gateway integration

🤝 Contributing

Contributions are welcome!
Fork the repository, raise issues, or submit pull requests.

📄 License

This project is intended for educational purposes.
<<<<<<< HEAD
Free to modify and extend.
=======
Free to modify and extend.
>>>>>>> 858617f52d7b293272fd561c17641053a5e482c5
