from flask import Flask, render_template, request, redirect
import sys
import os
import psycopg2

db_config = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else "user=postgres password=password"


def create_account(username, password):
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("INSERT INTO users VALUES (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    conn.close()
    #TODO: Replace this with a redirect
    return render_template("index.html", success=True)

def valid_login(username, password):
    #if username in db already, return false, else true
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s;", (username, ))
    account = cur.fetchone()
    conn.close()
    if account is None:
        return True
    else:
        return False

def invalid_account():
    return "<p>This is not a valid account: Username already in system!</p>"

def initialize_db():
    #Create db tables
    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username varchar, password varchar);")
    conn.close
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
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(port)
    app.run(host="0.0.0.0",port=port)
