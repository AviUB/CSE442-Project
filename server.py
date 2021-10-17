from flask import Flask, render_template, request, redirect
import sys
import os
import psycopg2

db_config = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else "user=postgres password=password"
FAKE_DB = {"username":["u_name"], "password": ["testPassword"]}


def create_account(username, password):
    global FAKE_DB
    FAKE_DB["username"] = username
    FAKE_DB["password"] = password

    return render_template("index.html", success=True)

def valid_login(username, password):
    #if username in db already, return false, else true
    global FAKE_DB
    try:
        user_index = FAKE_DB["username"].index(username)
        if FAKE_DB["password"][user_index] == password:
            return True
    except ValueError:
        return False




def invalid_account():
    return "<p>This is not a valid account: Username already in system!</p>"

def initialize_db():
    global FAKE_DB
    #Create db tables
    FAKE_DB = {"username": [], "password": []}

    return True

app = Flask(__name__)

@app.route("/")
def sample_page():
    return render_template("index.html", success=None)
    

@app.route("/login", methods=["POST"])
def login():
    if valid_login(request.form["username"],
                   request.form["pw"]):
        return redirect("/userlogin")
    else:
        return redirect("/")
        
@app.route("/userlogin")
def user_login_page():
    return render_template("userlogin.html")

if __name__=="__main__":

    initialize_db()
    # CREATE A TEST LOGIN
    create_account("u_name", "testPassword")
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(port)
    app.run(host="0.0.0.0",port=port)
