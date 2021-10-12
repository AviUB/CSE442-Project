from flask import Flask, render_template, request, jsonify
import psycopg2
import sys
import os

conn = psycopg2.connect(
   database="postgres", user='postgres', password='cse442project', host='127.0.0.1', port= '5432'
)
conn.autocommit = True

cur = conn.cursor()

# sql = '''CREATE database db''';

cur.execute("DROP TABLE IF EXISTS USERS")
sql ='''CREATE TABLE USERS(
   USERNAME VARCHAR(22) PRIMARY KEY,
   LOGINS INT,
   MEALSMADE INT,
   ACH1 BOOLEAN NOT NULL,
   ACH2 BOOLEAN NOT NULL,
   ACH3 BOOLEAN NOT NULL
)'''
cur.execute(sql)
cur.execute('''INSERT INTO USERS(USERNAME, LOGINS, MEALSMADE, ACH1, ACH2, ACH3) VALUES ('Jake', 0, 0, 'no', 'no', 'no')''')

#Closing the connection
# conn.close()

app = Flask(__name__)

def ach():
    return render_template("achievements.html")

def createJSON():
    cur.execute('''SELECT LOGINS FROM USERS WHERE USERNAME = 'Jake' ''')
    logins = cursor.fetchone()[0]
    cur.execute('''SELECT MEALSMADE FROM USERS WHERE USERNAME = 'Jake' ''')
    mealsMade = cursor.fetchone()[0]
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

@app.route("/")
def sample_page():
    # this is testing for database functionality
    # it will increment logins and meals made by one
    print()
    cur.execute('''UPDATE USERS SET LOGINS = LOGINS + 1 WHERE USERNAME = 'Jake' ''')
    cur.execute('''UPDATE USERS SET MEALSMADE = MEALSMADE + 1 WHERE USERNAME = 'Jake' ''')
    return "<p>added one to logins for jake</p>"

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


if __name__=="__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(port)
    app.run(host="0.0.0.0",port=port)
