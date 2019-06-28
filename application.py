import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from tempfile import mkdtemp

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash



from sqlalchemy_declarative import User, Event, Base, School, Student, Portfolio, Committee
from helpers import login_required, apology, database_access







app = Flask(__name__)
app.secret_key = os.urandom(642)
# sqlalchemy for dobby.db
# engine for database
dobb_engine = create_engine("sqlite:///dobby.db", echo=True, connect_args={'check_same_thread':False})
AppSession = sessionmaker(bind=dobb_engine)
dobb_metadata = MetaData(bind = dobb_engine)

# sqlalchemy for 'event'.db
engine = create_engine("sqlite:///databases/trial.db", echo=True, connect_args={'check_same_thread':False})
EventSession = sessionmaker(bind=engine)
event_metadata = MetaData(bind=engine)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
@login_required
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

        return redirect("/")

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
@login_required
def add_school():
    event_session = EventSession()
    if request.method == "POST":
        school_name = request.form.get("school_name")
        student_names = request.form.get("student_names").split(", ")

        school = School(name = school_name)

        if event_session.query(School).filter(School.name == school.name).one() is None:
            event_session.add(school)
            event_session.commit()
        else:
            school = event_session.query(School).filter(School.name == school.name).one()

        for name in student_names:
            student = Student(name = name, school_id = school.id)
            event_session.add(student)

        event_session.commit()
        return redirect("/")

    else:
        return render_template("add_school.html")

@app.route("/add_committee", methods=["POST", "GET"])
@login_required
def add_committee():
    event_session = EventSession()
    if request.method == "POST":
        committee_name = request.form.get("committee_name")
        portfolios_names = request.form.get("portfolio_names").split(", ")

        committee = Committee(name = committee_name)
        if event_session.query(Committee).filter(Committee.name == committee.name).one() is None:
            event_session.add(committee)
            event_session.commit()
        else:
            committee = event_session.query(Committee).filter(Committee.name == committee.name).one()

        for name in portfolios_names:
            portfolio = Portfolio(name = name, committee_id = committee.id)
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
        event = request.form.get("event")
        file_key = request.form.get("key")

        if not event or not key:
            return apology("Must provide all fields")

        if not check_password_hash(event.hash, file_key):
            return apology("Invalid Key")

        print('I am here')
        # request for event's database name and bind all variables to it
        # create new database for event
        engine = create_engine('sqlite:///databases/'+filename, connect_args={'check_same_thread': False}, echo=True)
        # configure global variables
        EventSession.configure(bind=engine)
        event_metadata.bind = engine

        session["event_id"] = event.id

        return redirect("/")

    else:
        events = app_session.query(Event).all()
        return render_template("file-select.html", events = events)


@app.route("/create")
@login_required
def create_database():
    '''new database'''
    if request.method == "POST":
        # get input from form
        event_name = request.form.get("event_name")
        key = request.form.get("key")

        if not event_name or not key:
            return apology("Event or key not given")

        filename = event_name.replace(" ", "_") + '.db'
        print(filename)
        # create connection to dobby.db
        app_session = AppSession()
        print('I am here')
        # insert new event into dobby.db
        event = Event(name = event_name, hash = generate_password_hash(password, "pbkdf2:sha256"), filename = filename)
        app_session.add(event)
        app_session.commit()

        # create new database for event
        engine = create_engine('sqlite:///databases/'+filename, echo=True, connect_args={'check_same_thread': False})
        # configure global variables
        EventSession.configure(bind=engine)
        event_metadata.bind = engine

        event_session = EventSession()

        # finally create tables for events
        event_metadata.create_all([Committee, Portfolio, School, Student])

        # remember database id
        session["event_id"] = event.id

        return redirect("/")

    else:
        return render_template("new_event.html")
