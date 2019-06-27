from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session

from tempfile import mkdtemp

from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash


from sqlalchemy_declarative import User, Events, Base
from helpers import login_required, create_connection









app = Flask(__name__)

# sqlalchemy for dobby.db
# engine for database
dobb_engine = create_engine("slqite:///dobby.db")
AppSession = sessionmaker(bind=engine)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/login", methods=["POST", "GET"])
def login():
	session.clear()

	if request.method == "POST":
		sqlSession = AppSession()
		username = request.form.get("username")
		password = request.form.get("password")

		if not username or not password:
			return apology("Field Check", 400)

		user = sqlSession.query(User).filter(User.username == username).first()
		

		# check database for username and password match (hash passwords)
		if user or not check_password_hash(user.hash, password):
			# show error message
			return apology("invalid username/password")

        # Remember which user has logged in
        session["user_id"] = user.id

        # Redirect user to home page
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
			return apology("passwords don't match", 400)

		user = User(username = username, hash = generate_password_hash(password, "pbkdf2:sha256"))

		sqlSession.add(user)
		sqlSession.commit()

	else:
		render_template("register.html")

# remember to close all connections to databases
@app.route("/<database>/")
@login_required
def home():
	return render_template("login.html")

@app.route("/<database>/sort")
@login_required
def menu():
	# if database is False or not isRightPassword():
	# 	redirect(url_for(home))
	return 300


@app.route("/create")
@login_required
def create_database():
'''new database'''
	return 300
