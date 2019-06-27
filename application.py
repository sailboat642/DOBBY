import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from tempfile import mkdtemp

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash



from sqlalchemy_declarative import User, Event, Base
from helpers import login_required, apology, database_access







app = Flask(__name__)
app.secret_key = os.urandom(642)
# sqlalchemy for dobby.db
# engine for database
dobb_engine = create_engine("sqlite:///dobby.db")
AppSession = sessionmaker(bind=dobb_engine)

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
    return redirect("/login")


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

@app.route("/select_event", methods=["POST", "GET"])
@login_required
def select_event():
    sqlSession = AppSession()
    if request.method == "POST":
        event = request.form.get("event")
        file_key = request.form.get("key")

        if not event or not key:
            return apology("Must provide all fields")

        if not check_password_hash(event.hash, file_key):
            return apology("Invalid Key")


        session["event_id"] = event.id

        return redirect("/")

    else:
        events = sqlSession.query(Event).all()
        return render_template("file-select.html", events = events)


@app.route("/create")
@login_required
def create_database():
    '''new database'''
    return 300
