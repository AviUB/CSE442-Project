from flask import Flask, render_template, request, redirect, url_for, session, abort
import sys
import os
import psycopg2
import hashlib

db_config = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else "user=postgres password=password"

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"] if "SECRET_KEY" in os.environ else 123456

def create_account(username, password, feet, inches, weight):
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()

    hashkey = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), bytes(username, 'utf-8'), 100000)
    cur.execute("INSERT INTO users (username, password, feet, inches, weight) VALUES (%s, %s, %s, %s, %s)", (username, hashkey.hex(), feet, inches, weight))
    
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

def get_user(username):
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("SELECT feet, inches, weight FROM users WHERE username=%s", (username, ))
    user = cur.fetchone()
    return user

def invalid_account():
    #TODO: Make a proper error and redirect
    return render_template("invalid_register.html")

def initialize_db():
    #Create db tables
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username varchar, password varchar, feet int, inches int, weight int);")
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
                                   request.form['password'],
                                   request.form['height_ft'],
                                   request.form['height_in'],
                                   request.form['weight'])
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

@app.route('/profile', methods=["GET", "POST"])
def profile():
    username = session['username']
    if request.method == "POST":
        type_ = request.form["type"]
        if type_ == "height":
            update_height(username, request.form["height_ft"], request.form["height_in"])
        elif type_ == "weight":
            update_weight(username, request.form["weight"])
        elif type_ == "password":
            update_password(username, request.form["current_pw"], request.form["new_pw"])
        else:
            pass
    user = get_user(username)
    if user != None:
        return render_template("profile.html", user={"username": username,"feet": user[0], "inches": user[1], "pounds": user[2]})
    else:
        print(f"Could NOT Find User: {username}")
        return render_template("profile.html")

def update_height(username, feet, inches):
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("UPDATE users SET feet=%s, inches=%s WHERE username=%s", (feet, inches, username))
    conn.commit()
    conn.close()

def update_weight(username, weight):
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("UPDATE users SET weight=%s WHERE username=%s", (weight, username))
    conn.commit()
    conn.close()

def update_password(username, current, new):
    if not verify_login(username, current):
        return
    hashkey = hashlib.pbkdf2_hmac('sha256', bytes(new, 'utf-8'), bytes(username, 'utf-8'), 100000).hex()
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("UPDATE users SET password=%s WHERE username=%s", (hashkey, username))
    conn.commit()
    conn.close()

@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")

if __name__=="__main__":
    setup = initialize_db()
    if setup:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
        print(port)
        app.run(host="0.0.0.0",port=port)
