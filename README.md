# 🎓 Student Management System

A Full Stack Student Management System built using **Python, Flask, MySQL, HTML, CSS, Bootstrap, and SQLAlchemy**. This project allows administrators to manage student records efficiently through a simple and responsive web interface.

---

## 🚀 Features

- 🔐 Admin Login & Logout
- 📊 Dashboard with Student Statistics
- ➕ Add New Student
- 📋 View All Students
- 🔍 Search Students by Name, Email, or Course
- ✏️ Edit Student Details
- 🗑️ Delete Student Records
- ✅ Form Validation
- 📧 Duplicate Email Validation
- 📁 Export Student Data to Excel
- 💬 Flash Messages for User Feedback
- 🔒 Protected Routes (Login Required)
- 📱 Responsive User Interface using Bootstrap

---

## 🛠️ Technologies Used

### Frontend
- HTML5
- CSS3
- Bootstrap 5
- Bootstrap Icons
- Jinja2 Templates

### Backend
- Python 3
- Flask
- SQLAlchemy

### Database
- MySQL

### Libraries
- Flask
- Flask-SQLAlchemy
- PyMySQL
- python-dotenv
- openpyxl

---

## 📂 Project Structure

```
Student-Management-System/
│
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── .env
│   ├── requirements.txt
│   └── .venv/
│
├── frontend/
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── index.html
│   │   ├── add_student.html
│   │   ├── edit_student.html
│   │   └── view_students.html
│   │
│   └── static/
│       ├── css/
│       ├── js/
│       └── images/
│
└── README.md
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/yourusername/student-management-system.git
```

### Navigate to Project

```bash
cd student-management-system/backend
```

### Create Virtual Environment

```bash
python -m venv .venv
```

### Activate Virtual Environment

#### Windows

```bash
.venv\Scripts\activate
```

#### macOS/Linux

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🗄️ Configure Database

Create a `.env` file inside the `backend` folder.

```env
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=student_db
```

---

## ▶️ Run the Application

```bash
python app.py
```

Open your browser:

```
http://127.0.0.1:5000
```

---

## 🔑 Admin Login

Default Credentials

**Username**

```
admin
```

**Password**

```
admin123
```

---

## 📊 Modules

- Dashboard
- Login
- Logout
- Add Student
- View Students
- Search Student
- Edit Student
- Delete Student
- Export to Excel

---

## 📸 Screenshots

Add screenshots here after uploading images.

Example:

- Login Page
- Dashboard
- Add Student
- View Students
- Edit Student

---

## 🔮 Future Enhancements

- PDF Export
- Pagination
- Course Management
- Student Profile Photo
- Email Notifications
- User Roles
- Cloud Deployment

---

## 👨‍💻 Author

**Balasubramanyam Charitha**

B.Tech Student

Aspiring Full Stack Python Developer

---

## 📜 License

This project is developed for learning purposes and personal portfolio.