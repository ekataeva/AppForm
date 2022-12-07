
from flask import flash, redirect, render_template, request, session
from functools import wraps
import sqlite3
from sqlite3 import Error


def create_connection():
    conn=None
    try:
        conn = sqlite3.connect('application.db')
    except Error as e:
        return apology("Db connection failed", e)
    return conn

def submit_app(conn, data):
    sql = ''' INSERT INTO apps VALUES (?, ?, ?, false, ?, ?, ?, ?) '''
    cur = conn.cursor()
    cur.executemany(sql, (data,))
    conn.commit()

def db_register(conn, data):
    sql = ''' INSERT INTO users (username, hash) VALUES (?, ?) '''
    cur = conn.cursor()
    cur.executemany(sql, data)
    conn.commit()
    return cur.lastrowid

def db_querry(conn, sql, data):
    cur = conn.cursor()
    cur.execute(sql, (data,))
    rows = cur.fetchall()
    return rows

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """  Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters  """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


