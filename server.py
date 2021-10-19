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
    return redirect(url_for("user_login_page"))

def valid_login(username, password):
    #if username in db already, return false, else true
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
    if account[0] == username and account[1] == password:
        print("ACCT FOUND")
        return True
    else:
        print("ACCT NOT FOUND")
        return False

def invalid_account():
    #TODO: Make a proper error and redirect
    return "<p>This is not a valid account: Username already in system!</p>"

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
        return redirect("/userlogin")
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

if __name__=="__main__":
    setup = initialize_db()
    if setup:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
        print(port)
        app.run(host="0.0.0.0",port=port)
