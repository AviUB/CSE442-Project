from flask import Flask, render_template, request, redirect, url_for, session, abort
import sys
import os
import psycopg2
import hashlib

db_config = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else "user=postgres password=password"

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"] if "SECRET_KEY" in os.environ else 123456

def create_account(username, password):
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    hashkey = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), bytes(username, 'utf-8'), 100000)
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashkey.hex()))
    conn.commit()
    conn.close()
    return redirect(url_for("sample_page"))

def valid_login(username, password):
    #if username in db already, return false, else true
    if len(password) < 8 or len(password) > 1024:
        return False
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s;", (username, ))
    account = cur.fetchone()
    conn.commit()
    conn.close()
    if account is None:
        return True
    else:
        return False

def verify_login(username, password):
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s;", (username, ))
    account = cur.fetchone()
    if account is None:
        return False
    passhash = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), bytes(username, 'utf-8'), 100000)
    if account[0] == username and account[1] == passhash.hex():
        return True
    else:
        return False

def invalid_account():
    #TODO: Make a proper error and redirect
    return render_template("invalid_register.html")

def initialize_db():
    #Create db tables
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username varchar, password varchar);")
    conn.commit()
    conn.close()
    return True

@app.route("/")
def sample_page():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    if verify_login(request.form["username"],
                   request.form["pw"]):
        session['username'] = request.form["username"]
        return redirect(url_for("mealspage"))
    else:
        
        return redirect("/")
        
@app.route("/userlogin")
def user_login_page():
    return render_template("userlogin.html")

@app.route("/create_account", methods=['GET','POST'])
def create_account_page():
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return create_account(request.form['username'],
                                   request.form['password'])
        else:
            return invalid_account()
    else:
        return render_template("create_account.html")

@app.route('/calendar/<username>')
def dummycalendarpage(username):
    if 'username' in session and session['username'] == username:
        return '<p>This is the calendar page for: ' + username + '.</p>'
    else:
        abort(404)
        return 'Never returned'
    
@app.route('/mealspage')
def mealspage():
    if 'username' in session:
        return render_template('mealspage.html')
    else:
        abort(404)
        return 'Never returned'

@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")

@app.route('/passhash/<username>')
def getHash(username):
    if 'username' in session and session['username'] == username:
        conn = psycopg2.connect(db_config)
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s;", (username, ))
        account = cur.fetchone()
        if account is None:
            abort(404)
            return 'Never returned'
        return '<p>This is the hashed password for ' + username + ': ' + account[1] + '</p>'
    else:
        abort(404)
        return 'Never returned'

if __name__=="__main__":
    setup = initialize_db()
    if setup:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
        print(port)
        app.run(host="0.0.0.0",port=port)
