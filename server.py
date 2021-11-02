from flask import Flask, render_template, request, redirect, url_for
import sys
import os
import psycopg2

db_config = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else "user=postgres password=cse442project"

curUser = ""

# conn = psycopg2.connect(database="postgres", user='postgres', password='cse442project', host='127.0.0.1', port= '5432')


#Closing the connection
# conn.close()

app = Flask(__name__)



def create_account(username, password):
    #conn = psycopg2.connect(db_config, sslmode='require')
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))

    cur.execute('''INSERT INTO ACHS(USERNAME, LOGINS, MEALSMADE, ACH1, ACH2, ACH3) VALUES (%s, 0, 0, 'no', 'no', 'no')''', (username))

    conn.commit()
    conn.close()
    return redirect(url_for("sample_page"))

def valid_login(username, password):
    #if username in db already, return false, else true
    if len(password) < 8:
        return False
    #conn = psycopg2.connect(db_config, sslmode='require')
    conn = psycopg2.connect(db_config)
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

def invalid_account():
    #TODO: Make a proper error and redirect
    return render_template("invalid_register.html")

def initialize_db():
    #Create db tables
    #conn = psycopg2.connect(db_config, sslmode='require')
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username varchar, password varchar)")

    cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("Jake", "password"))

    #cur.execute("DROP TABLE IF EXISTS ACHS")
    sql ="CREATE TABLE IF NOT EXISTS ACHS(USERNAME VARCHAR(22) PRIMARY KEY, LOGINS INT, MEALSMADE INT, ACH1 BOOLEAN NOT NULL, ACH2 BOOLEAN NOT NULL, ACH3 BOOLEAN NOT NULL)"
    cur.execute(sql)
    #cur.execute("INSERT INTO ACHS(USERNAME, LOGINS, MEALSMADE, ACH1, ACH2, ACH3) VALUES ('Jake', 0, 0, 'no', 'no', 'no')")

    conn.commit()
    conn.close()
    return True


def ach():
    return render_template("achievements.html")

def createJSON():
    cur.execute("SELECT LOGINS FROM ACHS WHERE USERNAME = %s ", curUser)
    logins = cur.fetchone()[0]
    cur.execute("SELECT MEALSMADE FROM ACHS WHERE USERNAME = %s ", curUser)
    mealsMade = cur.fetchone()[0]
    ach1 = "0"
    ach2 = "0"
    ach3 = "0"
    if (logins > 0) and (logins > 2):
        ach1 = "1"
        ach3 = "1"
    elif (logins > 0):
        ach1 = "1"
    if (mealsMade > 0):
        ach2 = "1"
    return {"1": ["Would you look at the time!", "Successfully logged in for the first time.", ach1],
                        "2": ["Here comes the plane!", "Create your first meal.", ach2],
                        "3": ["Who's hungry?", "Login on 3 separate occasions.", ach3]}


@app.route("/achievements", methods=['GET','POST'])
def achievements():

    if request.method == 'POST':
        return jsonify(createJSON())
    else:
        return ach()

@app.route("/achievements.css")
def achOne():
    return render_template("achievements.css")

@app.route("/achievements.js")
def achTwo():
    return render_template("achievements.js")


@app.route("/")
def sample_page():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    if verify_login(request.form["username"],
                   request.form["pw"]):

        #conn = psycopg2.connect(db_config, sslmode='require')
        conn = psycopg2.connect(db_config)
        cur = conn.cursor()

        cur.execute('''UPDATE ACHS SET LOGINS = LOGINS + 1 WHERE USERNAME = %s ''', request.form["username"])

        conn.commit()
        conn.close()

        curUser = request.form["username"]
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

@app.route('/aboutus')
def aboutus():
    return render_template("aboutus.html")

if __name__=="__main__":
    setup = initialize_db()
    if setup:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
        print(port)
        app.run(host="0.0.0.0",port=port)
