from flask import Flask, render_template, request, redirect, url_for
import sys
import os
import psycopg2

db_config = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else "user=postgres password=password"

app = Flask(__name__)

def create_account(username, password):
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    conn.close()
    return redirect(url_for("sample_page"))

def valid_login(username, password):
    #if username in db already, return false, else true
    if len(password) < 8:
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
    if account[0] == username and account[1] == password:
        print("ACCT FOUND")
        return True
    else:
        print("ACCT NOT FOUND")
        return False

def get_user(username):
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("SELECT feet inches weight FROM users WHERE username=%s", (username, ))
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
    
@app.route('/mealspage')
def mealspage():
    return render_template('mealspage.html')

@app.route('/profile', methods=["GET", "POST"])
def profile():
    username = ""
    if request.method == "POST":
        type_ = request.form["type"]
        if type_ == "height":
            update_height(username, request.form["height-feet"], request.form["height-inches"])
        elif type_ == "weight":
            update_weight(username, request.form["weight-pounds"])
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
        
def update_height(user, feet, inches):
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("UPDATE users SET feet=%d inches=%d WHERE username=%s", (feet, inches, username))
    conn.commit()
    conn.close()

def update_weight(user, weight):
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("UPDATE users SET weight=%d WHERE username=%s", (weight, username))
    conn.commit()
    conn.close()

def update_password(user, current, new):
    if not verify_login(user, current):
        return
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("UPDATE users SET password=%s WHERE username=%s", (new, username))
    conn.commit()
    conn.close()

if __name__=="__main__":
    setup = initialize_db()
    if setup:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
        print(port)
        app.run(host="0.0.0.0",port=port)
