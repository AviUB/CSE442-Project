from flask import Flask, render_template, request
import sys
import os
import psycopg2

def create_account(username, password):
    return"<p>"+"You submitted a create account form: "+username+", "+password+"</p>"

def valid_login(username, password):
    #if username in db already, return false, else true
    return True

def invalid_account():
    return "<p>This is not a valid account: Username already in system!</p>"

def initialize_db():
    #Create db tables
    return True

app = Flask(__name__)

@app.route("/")
def sample_page():
    return render_template("index.html")

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
    initialize_db()
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(port)
    app.run(host="0.0.0.0",port=port)
