import os
import re
from urllib.parse import quote_plus
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from sqlalchemy import or_
from models import db, Student
from openpyxl import Workbook
from io import BytesIO

# Load environment variables
load_dotenv()

# Template folder path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, "..", "frontend", "templates")

# Create Flask app
app = Flask(__name__, template_folder=TEMPLATE_DIR)
app.secret_key = "student_management_secret_key"

# Database configuration
password = quote_plus(os.getenv("DB_PASSWORD"))

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{password}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# ---------------- LOGIN REQUIRED ----------------
def login_required():

    if not session.get("admin"):
        flash("Please login first!", "warning")
        return False

    return True
# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])

def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "admin" and password == "admin123":

            session["admin"] = True
            flash("Login Successful!", "success")

            return redirect(url_for("home"))

        flash("Invalid Username or Password!", "danger")

    return render_template("login.html")

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.clear()

    flash("Logged out successfully!", "info")

    return redirect(url_for("login"))

# ---------------- HOME PAGE ----------------

@app.route("/")
def home():

    if not login_required():
        return redirect(url_for("login"))
    total_students = Student.query.count()
    male_students = Student.query.filter_by(gender="Male").count()
    female_students = Student.query.filter_by(gender="Female").count()

    return render_template(
    "index.html",
    total_students=total_students,
    male_students=male_students,
    female_students=female_students
)

# ---------------- ADD STUDENT ----------------
@app.route("/add", methods=["GET", "POST"])
def add_student():

    if not login_required():
        return redirect(url_for("login"))

    if request.method == "POST":

        name = request.form["name"].strip()
        age = int(request.form["age"])
        gender = request.form["gender"]
        email = request.form["email"].strip()
        course = request.form["course"].strip()
        phone = request.form["phone"].strip()
        address = request.form["address"].strip()

        # Name Validation
        if not re.fullmatch(r"[A-Za-z ]+", name):
            flash("Name should contain only letters and spaces.", "danger")
            return redirect(url_for("add_student"))

        # Age Validation
        if age < 16 or age > 100:
            flash("Age must be between 16 and 100.", "danger")
            return redirect(url_for("add_student"))

        # Phone Validation
        if not re.fullmatch(r"\d{10}", phone):
            flash("Phone number must contain exactly 10 digits.", "danger")
            return redirect(url_for("add_student"))

        # Duplicate Email Check
        existing_student = Student.query.filter_by(email=email).first()

        if existing_student:
            flash("Email already exists!", "danger")
            return redirect(url_for("add_student"))

        student = Student(
            name=name,
            age=age,
            gender=gender,
            email=email,
            course=course,
            phone=phone,
            address=address
        )

        db.session.add(student)
        db.session.commit()

        flash("Student added successfully!", "success")

        return redirect(url_for("view_students"))

    return render_template("add_student.html")


# ---------------- VIEW STUDENTS ----------------
@app.route("/students")
def view_students():

    if not login_required():
        return redirect(url_for("login"))

    students = Student.query.all()

    return render_template(
        "view_students.html",
        students=students
    )


# ---------------- SEARCH STUDENT ----------------
@app.route("/search")
def search_student():

    if not login_required():
        return redirect(url_for("login"))

    query = request.args.get("query", "")

    students = Student.query.filter(
        or_(
            Student.name.ilike(f"%{query}%"),
            Student.email.ilike(f"%{query}%"),
            Student.course.ilike(f"%{query}%")
        )
    ).all()

    return render_template(
        "view_students.html",
        students=students
    )


# ---------------- EXPORT TO EXCEL ----------------
@app.route("/export")
def export_students():

    if not login_required():
        return redirect(url_for("login"))
    students = Student.query.all()

    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Students"

    # Header row
    sheet.append([
        "ID",
        "Name",
        "Age",
        "Gender",
        "Email",
        "Course",
        "Phone",
        "Address"
    ])

    # Student data
    for student in students:
        sheet.append([
            student.id,
            student.name,
            student.age,
            student.gender,
            student.email,
            student.course,
            student.phone,
            student.address
        ])

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    return send_file(
        output,
        as_attachment=True,
        download_name="students.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )


# ---------------- EDIT STUDENT ----------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):

    if not login_required():
        return redirect(url_for("login"))

    student = Student.query.get_or_404(id)

    if request.method == "POST":

        name = request.form["name"].strip()
        age = int(request.form["age"])
        gender = request.form["gender"]
        email = request.form["email"].strip()
        course = request.form["course"].strip()
        phone = request.form["phone"].strip()
        address = request.form["address"].strip()

        # Name Validation
        if not re.fullmatch(r"[A-Za-z ]+", name):
            flash("Name should contain only letters and spaces.", "danger")
            return redirect(url_for("edit_student", id=id))

        # Age Validation
        if age < 16 or age > 100:
            flash("Age must be between 16 and 100.", "danger")
            return redirect(url_for("edit_student", id=id))

        # Phone Validation
        if not re.fullmatch(r"\d{10}", phone):
            flash("Phone number must contain exactly 10 digits.", "danger")
            return redirect(url_for("edit_student", id=id))

        # Duplicate Email Check
        existing_student = Student.query.filter(
            Student.email == email,
            Student.id != id
        ).first()

        if existing_student:
            flash("Email already exists!", "danger")
            return redirect(url_for("edit_student", id=id))

        student.name = name
        student.age = age
        student.gender = gender
        student.email = email
        student.course = course
        student.phone = phone
        student.address = address

        db.session.commit()

        flash("Student updated successfully!", "warning")

        return redirect(url_for("view_students"))

    return render_template(
        "edit_student.html",
        student=student
    )


# ---------------- DELETE STUDENT ----------------
@app.route("/delete/<int:id>")
def delete_student(id):

    if not login_required():
        return redirect(url_for("login"))

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    flash("Student deleted successfully!", "danger")

    return redirect(url_for("view_students"))


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)