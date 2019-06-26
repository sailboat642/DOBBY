from flask import Flask, render_template, session, url_for, request, redirect
import sqlite3

app = Flask(__name__)

@app.route("/login")
def login():
	session.clear()

	if request.method == "POST":
		username = request.form.get("username")
		password = request.form.get("password")

		if not username:
			return 403

		if not password:
			return 403



		# check database for username and password match (hash passwords)

		return render_template("index.html")

@app.route("/<database>/")
@login_required
def home():
	return render_template("login.html")

@app.route("/<database>/group-edit")
@login_required
def menu():
	# if database is False or not isRightPassword():
	# 	redirect(url_for(home))
