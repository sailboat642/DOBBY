import os
import csv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from tempfile import mkdtemp

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash



from sqlalchemy_declarative import User, Event, Base, School, Student, Portfolio, Committee, AppBase
from helpers import login_required, apology, database_access




app = Flask(__name__)
app.secret_key = os.urandom(642)

# sqlalchemy for dobby.db
# engine for database
dobb_engine = create_engine("sqlite:///dobby.db", echo=True, connect_args={'check_same_thread':False})
AppSession = sessionmaker(bind=dobb_engine)
dobb_metadata = MetaData(bind=dobb_engine)

# sqlalchemy for 'event'.db
EventSession = sessionmaker()
event_metadata = MetaData()

UPLOAD_FOLDER = "/input_files"

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
@database_access
def home():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    session.clear()
    if request.method == "POST":
        sqlSession = AppSession()
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return apology("Field Check")

        user = sqlSession.query(User).filter(User.username == username).first()

        if not user or not check_password_hash(user.hash, password):
            return apology("Invalid username/password")

        session["user_id"] = user.id
        session["user"] = user.username

        return redirect("/select_event")

    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        sqlSession = AppSession()

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username or not password or not username:
            return apology("Field Check", 400)

        if password != confirmation:
            return apology("Passwords don't match", 400)

        if sqlSession.query(User).filter(User.username == username).first():
            return apology("username exists")

        user = User(username = username, hash = generate_password_hash(password, "pbkdf2:sha256"))

        sqlSession.add(user)
        sqlSession.commit()

        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/add_school", methods=["POST", "GET"])
@database_access
def add_school():
    event_session = EventSession()
    if request.method == "POST":
        student_list_file = request.files["file"]
        school_name = request.form.get("school_name")
        school_grade = request.form.get("school_grade") 
        student_data = request.form.get("student_names")

        if student_list_file is not None:
            student_list_file.save(f"input_files/{student_list_file.filename}")
            with open(f"input_files/{student_list_file.filename}") as csv_file:
                data = csv.reader(csv_file, delimiter = ',')

                rows = []
                for row in data:
                    rows.append(row)

            school = School(name=rows[0][0], grade=rows[0][1])
            student_data = []
            for i in range(1, len(rows)):
                student_data.append(rows[i])
        else:        
            school = School(name = school_name, grade = school_grade)

        if event_session.query(School).filter(School.name == school.name).first() is None:
            event_session.add(school)
            event_session.commit()
        else:
            school = event_session.query(School).filter(School.name == school.name).first()
            school.grade = school_grade

        for row in student_data:
            student = Student(name = row[0], school_id = school.id, gender = row[1])
            event_session.add(student)

        event_session.commit()
        return redirect("/")

    else:
        return render_template("add_school.html")

@app.route("/add_committee", methods=["POST", "GET"])
@database_access
def add_committee():
    event_session = EventSession()
    if request.method == "POST":
        committee_name = request.form.get("committee_name")
        portfolios_raw = request.form.get("portfolio_names").split("\n")

        committee = Committee(name = committee_name)
        if event_session.query(Committee).filter(Committee.name == committee.name).first() is None:
            event_session.add(committee)
            event_session.commit()
        else:
            committee = event_session.query(Committee).filter(Committee.name == committee.name).first()

        for string in portfolios_raw:
            info = string.split(", ")
            portfolio = Portfolio(name = info[0], committee_id = committee.id, rank = info[1])
            event_session.add(portfolio)

        event_session.commit()
        return redirect("/")

    else:
        return render_template("add_committee.html")

@app.route("/select_event", methods=["POST", "GET"])
@login_required
def select_event():
    app_session = AppSession()
    if request.method == "POST":
        app_session = AppSession()
        name = request.form.get("name")
        file_key = request.form.get("key")


        if not name or not file_key:
            return apology("Must provide all fields")

        event = app_session.query(Event).filter(Event.name == name).first()

        if event is None:
            return apology("could not find event")

        if not check_password_hash(event.hash, file_key):
            return apology("Invalid Key")

        # request for event's database name and bind all variables to it
        # create new database for event
        engine = create_engine(f'sqlite:///databases/{event.filename}', connect_args={'check_same_thread': False}, echo=True)
        # configure global variables
        EventSession.configure(bind=engine)

        session["event_id"] = event.id

        return redirect("/")

    else:
        events = app_session.query(Event).all()
        return render_template("file-select.html", events = events)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create_database():
    '''new database'''
    if request.method == "POST":
        # get input from form
        event_name = request.form.get("event_name")
        key = request.form.get("key")
        confirmation = request.form.get("confirmation")

        if not event_name or not key:
            return apology("Event or key not given")

        if key != confirmation:
            return apology("confirmation does not match")

        filename = event_name.replace(" ", "_").replace("/", "-") + '.db'
        # create connection to dobby.db
        app_session = AppSession()

        # insert new event into dobby.db
        event = Event(name = event_name, hash = generate_password_hash(key, "pbkdf2:sha256"), filename = filename)
        app_session.add(event)

        # create new database for event
        engine = create_engine(f"sqlite:///databases/{filename}", echo=True, connect_args={'check_same_thread': False})
        # configure global variables
        EventSession.configure(bind=engine)

        # finally create tables for events
        Base.metadata.create_all(engine)

        app_session.commit()

        # remember database id
        session["event_id"] = event.id

        app_session.close()

        return redirect("/")

    else:
        return render_template("new_event.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/view")
@database_access
def view():
    session = EventSession()

    rows = session.query(Student.id, Portfolio.name, Student.name, Committee.name).join(Student, Committee).order_by(Student.id).all()
    return render_template("view.html", rows=rows)


@app.route("/sort_all", methods=["POST"])
@database_access
def sort_all():
    if request.method == "POST":
        event_session = EventSession()
        portfolios = event_session.query(Portfolio).order_by(Portfolio.rank).all()
        students = event_session.query(Student).order_by(School.grade).all()

        count = event_session.query(func.count(Student.id)).first()[0]

        for i in range(count):
            portfolios[i].student_id = students[i].id

        event_session.commit()
        return redirect("/")

    # under construction
    # if request.method == "POST":
        # event_session = EventSession()
        # shuffle portfolio_id
        # get schools+portfolios from database order by id and grade
        # portfolios = event_session.query(Portfolio, Committee).join(Committee).order_by(Portfolio.rank, Committe.id).all()
        # return render_template("viewv.html")

        # get committees
        # loop and get each committee's portfolios
        # for students iterate through committees and assign portfolios
        # commit

        # sorted by rank, as many different committees, fair sort?