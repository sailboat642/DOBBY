import sqlite3

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, create_connection

app = Flask(__name__)

dobby_conn = conn.create_connection("./dobby.db")
dobby_curs = dobby_conn.cursor()
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
		username = request.form.get("username")
		password = request.form.get("password")

		if not username or not password:
			return 403

		rows = dobby_curs.execute("SELECT * FROM users WHERE name = ?", username)
		

		# check database for username and password match (hash passwords)
		if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password)
            return apology("invalid username and/or password", 403)

		return render_template("index.html")

# remember to close all connections to databases
@app.route("/<username>/<database>/")
@login_required
def home():
	return render_template("login.html")

@app.route("/<database>/group-edit")
@login_required
def menu():
	# if database is False or not isRightPassword():
	# 	redirect(url_for(home))


@app.route("/create")
@login_required
def create_database():
'''new database'''
	name = request.form.get("filename")
	filename = "./databases/" + name + ".db"
	try:
    	conn = sqlite3.connect(filename)
    except Error as e:
    	# return this error to webpage instead
        print(e)
    
    conn.execute
