from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import create_connection, submit_app, db_register, db_querry, apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
@login_required
def index():

    if request.method == "POST":
        # Submit an application and show history
        name = request.form.get("name")
        lastname = request.form.get("lastname")
        patronymic = request.form.get("patronymic")
        phonenumber = request.form.get("phonenumber")
        application = request.form.get("application")
        now = datetime.now()
        app = (session["user_id"], application, now, name, lastname, patronymic, phonenumber)
        conn = create_connection()
        with conn:
            submit_app(conn, app)
        return redirect("/history")

    else:
        # Show application form
        return render_template("form.html")


@app.route("/history")
@login_required
def history():
    sql = "SELECT * FROM apps WHERE user_id = ?"
    id = session["user_id"]
    conn = create_connection()
    with conn:
        rows = db_querry(conn, sql, id)
        print(rows)
        return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():

    # Forget any user_id
    session.clear()

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 403)

        # Query database for username
        conn = create_connection()
        sql = "SELECT * FROM users WHERE username = ?"
        with conn:
            rows = db_querry(conn, sql, username)

            # Ensure username exists and password is correct
            if len(rows) != 1 or not check_password_hash(rows[0][2], password):
                return apology("invalid username and/or password", 403)

            # Remember which user has logged in
            session["user_id"] = rows[0][0]

            # Redirect user to home page
            return redirect("/")

    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET","POST"])
def register():
    """Register user"""

    # Submit the user’s input via POST to /register.
    if request.method == "POST":

        # Require that a user input a username, implemented as a text field whose name is username.
        username = request.form.get("username")

        conn = create_connection()
        sql = " SELECT * FROM users WHERE username = ?"
        with conn:
            rows = db_querry(conn, sql, username)

        # Render an apology if the user’s input is blank or the username already exists.
        if not username or len(rows) >= 1:
            return apology("Invalid username. Try again", 403)

        # Require that a user input a password, implemented as a text field whose name is password,
        # and then that same password again, implemented as a text field whose name is confirmation.
        password = request.form.get("password")
        confirm = request.form.get("confirm")

        # Render an apology if either input is blank or the passwords do not match.
        if not password:
            return apology("Invalid password. Try again", 403)
        if password != confirm:
            return apology("Passwords do not match. Try again", 403)

        # Hash the user’s password with generate_password_hash
        hash = generate_password_hash(password)

        # INSERT the new user into users, storing a hash of the user’s password
        conn = create_connection(db)
        with conn:
            id = db_register(conn, (username, hash))

        session["user_id"] = id
        flash("Registered!")

        return redirect("/")

    else:
        return render_template("register.html")