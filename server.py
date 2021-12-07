from flask import Flask, render_template, request, redirect, url_for, session, abort, jsonify
import sys
import os
import psycopg2
import hashlib
import urllib.request
import urllib.parse
import json

db_config = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else "user=postgres password=cse442project"

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"] if "SECRET_KEY" in os.environ else "123456"

def create_account(username, password, feet, inches, weight, age, gend, act):

    #conn = psycopg2.connect(db_config, sslmode='require')
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    hashkey = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), bytes(username, 'utf-8'), 100000)
    cur.execute("INSERT INTO users (username, password, feet, inches, weight, age, gender, activity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (username, hashkey.hex(), feet, inches, weight, age, gend, act))


    cur.execute("INSERT INTO ACHS(USERNAME, LOGINS, MEALSMADE, ACH1, ACH2, ACH3) VALUES (%s, 0, 0, 'no', 'no', 'no')", (username,))


    #strng = "initialized food item space                                                             "
    #cur.execute("INSERT INTO bmeals(USERNAME, DATE, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, "10-10-1960", 0, strng, strng, strng, strng, strng, strng, strng, strng, strng))
    #cur.execute("INSERT INTO lmeals(USERNAME, DATE, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, 0, strng, strng, strng, strng, strng, strng, strng, strng, strng))
    #cur.execute("INSERT INTO dmeals(USERNAME, DATE, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, 0, strng, strng, strng, strng, strng, strng, strng, strng, strng))
    #cur.execute("INSERT INTO smeals(USERNAME, DATE, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, 0, strng, strng, strng, strng, strng, strng, strng, strng, strng))


    conn.commit()
    conn.close()
    return redirect(url_for("sample_page"))

def valid_login(username, password):
    #if username in db already, return false, else true
    if len(password) < 8 or len(password) > 1024:
        return False
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

#ensure given user actually exists
def verify_user(username):
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = %s;", (username, ))
    account = cur.fetchone()
    conn.commit()
    conn.close()
    if account is None:
        return False
    else:
        return True
    
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
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    #cur.execute("DROP TABLE IF EXISTS users")
    #feet, inches, weight, age, gender(0-male, 1-female, 2-other), activity(1-little,2-light,3-moderate,4-very active,5-extra active)
    cur.execute("CREATE TABLE IF NOT EXISTS users (username varchar, password varchar, feet int, inches int, weight int, age int, gender int, activity int)")

    #cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("Jake", "password"))

    #cur.execute("DROP TABLE IF EXISTS ACHS")
    sql ="CREATE TABLE IF NOT EXISTS ACHS(USERNAME VARCHAR PRIMARY KEY, LOGINS INT, MEALSMADE INT, ACH1 BOOLEAN NOT NULL, ACH2 BOOLEAN NOT NULL, ACH3 BOOLEAN NOT NULL)"
    cur.execute(sql)
    #cur.execute("INSERT INTO ACHS(USERNAME, LOGINS, MEALSMADE, ACH1, ACH2, ACH3) VALUES ('Jake', 0, 0, 'no', 'no', 'no')")

    #cur.execute("DROP TABLE IF EXISTS bmeals")
    #cur.execute("DROP TABLE IF EXISTS lmeals")
    #cur.execute("DROP TABLE IF EXISTS dmeals")
    #cur.execute("DROP TABLE IF EXISTS smeals")
    #there is now a date associated with each set of foods that make up a meal
    #go into the code to make sure we add this date column to all appropriate places
    cur.execute("CREATE TABLE IF NOT EXISTS bmeals(USERNAME VARCHAR, DATE VARCHAR, NOMEALS INT, M1 VARCHAR, M2 VARCHAR, M3 VARCHAR, M4 VARCHAR, M5 VARCHAR, M6 VARCHAR, M7 VARCHAR, M8 VARCHAR)")
    cur.execute("CREATE TABLE IF NOT EXISTS lmeals(USERNAME VARCHAR, DATE VARCHAR, NOMEALS INT, M1 VARCHAR, M2 VARCHAR, M3 VARCHAR, M4 VARCHAR, M5 VARCHAR, M6 VARCHAR, M7 VARCHAR, M8 VARCHAR)")
    cur.execute("CREATE TABLE IF NOT EXISTS dmeals(USERNAME VARCHAR, DATE VARCHAR, NOMEALS INT, M1 VARCHAR, M2 VARCHAR, M3 VARCHAR, M4 VARCHAR, M5 VARCHAR, M6 VARCHAR, M7 VARCHAR, M8 VARCHAR)")
    cur.execute("CREATE TABLE IF NOT EXISTS smeals(USERNAME VARCHAR, DATE VARCHAR, NOMEALS INT, M1 VARCHAR, M2 VARCHAR, M3 VARCHAR, M4 VARCHAR, M5 VARCHAR, M6 VARCHAR, M7 VARCHAR, M8 VARCHAR)")


    conn.commit()

    """
    sql = "SELECT * FROM users WHERE username = 'Jake' and not exists ( SELECT * FROM users WHERE username = 'Jake') union all SELECT * FROM users WHERE username = 'Jake';"
    cur.execute(sql)
    conn.commit()
    t_or_f = cur.fetchone()[0]
    print(t_or_f)
    if t_or_f == "t":

        # then don't add myself to database
        print("IT WAS TRUE")
    elif t_or_f == "f": """




    #hashkey = hashlib.pbkdf2_hmac('sha256', bytes("blahblah", 'utf-8'), bytes("Jake", 'utf-8'), 100000)
    #cur.execute("INSERT INTO users (username, password, feet, inches, weight, age, gender, activity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", ("Jake", hashkey.hex(), 5, 8, 180, 21, 0, 2))


    #cur.execute("INSERT INTO ACHS(USERNAME, LOGINS, MEALSMADE, ACH1, ACH2, ACH3) VALUES (%s, 0, 0, 'no', 'no', 'no')", ("Jake",))

    #strng = "initialized food item space                                                             "
    #cur.execute("INSERT INTO bmeals(USERNAME, DATE, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ("Jake", "10-10-1960", 0, strng, strng, strng, strng, strng, strng, strng, strng))
    #cur.execute("INSERT INTO lmeals(USERNAME, DATE, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ("Jake", "10-10-1960", 0, strng, strng, strng, strng, strng, strng, strng, strng))
    #cur.execute("INSERT INTO dmeals(USERNAME, DATE, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ("Jake", "10-10-1960", 0, strng, strng, strng, strng, strng, strng, strng, strng))
    #cur.execute("INSERT INTO smeals(USERNAME, DATE, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ("Jake", "10-10-1960", 0, strng, strng, strng, strng, strng, strng, strng, strng))
    #conn.commit()
        # then add myself to database
    """    print("IT WAS FALSE")
    else:
        print("SOMETHING WENT WRONG") """

    #cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("Jake", "password"))
    #hashkey = hashlib.pbkdf2_hmac('sha256', bytes("password", 'utf-8'), bytes("Jake", 'utf-8'), 100000)
    #cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("Jake", hashkey.hex()))

    #cur.execute("INSERT INTO ACHS(USERNAME, LOGINS, MEALSMADE, ACH1, ACH2, ACH3) VALUES ('Jake', 0, 0, 'no', 'no', 'no')")
    #strng = "initialized food item space                                                             "
    #cur.execute("INSERT INTO bmeals(USERNAME, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ("Jake", 0, strng, strng, strng, strng, strng, strng, strng, strng))
    #cur.execute("INSERT INTO lmeals(USERNAME, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ("Jake", 0, strng, strng, strng, strng, strng, strng, strng, strng))
    #cur.execute("INSERT INTO dmeals(USERNAME, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ("Jake", 0, strng, strng, strng, strng, strng, strng, strng, strng))
    #cur.execute("INSERT INTO smeals(USERNAME, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", ("Jake", 0, strng, strng, strng, strng, strng, strng, strng, strng))

    #conn.commit()
    conn.close()
    return True

@app.route("/")
def sample_page():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():
    if verify_login(request.form["username"],
                   request.form["pw"]):

        conn = psycopg2.connect(db_config)
        cur = conn.cursor()
        print("updating logins\n")
        cur.execute("UPDATE ACHS SET LOGINS = LOGINS + 1 WHERE USERNAME = %s", (request.form["username"],))

        conn.commit()
        conn.close()
        print("updated logins\n")

        ''' we get errors here '''
        session['username'] = request.form["username"]
        print("yay no errors\n")
        '''       !!!!!!   something happens here...     !!!!!!!!!!     '''
        #return redirect(url_for("mealspage"))
        '''       !!!!!!   something happens here...     !!!!!!!!!!     '''
        return redirect(url_for("calendar"))
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
                                   request.form['weight'], request.form['age'], request.form['gender'], request.form['act'])
        else:
            return invalid_account()
    else:
        return render_template("create_account.html")
"""
@app.route('/calendar/<username>')
def dummycalendarpage(username):
    if 'username' in session and session['username'] == username:
        return '<p>This is the calendar page for: ' + username + '.</p>'
    else:
        abort(404)
        return 'Never returned'
"""



def getAllMeals():
    #this method will get the username and then send all of the meals in a nice json back to the client
    username = session['username']
    returnJSON = {"1": [""],"2": [""],"3": [""],"4": [""],"5": [""],"6": [""],"7": [""],"8": [""]}
    returnJSON = {"s": [""]}
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM smeals WHERE USERNAME = %s", (username,))
    conn.commit()
    smeals = cur.fetchall()
    #smeals is a list of tuples for rows

    snackDict = {"11-11-1911": ["", "", "", "", "", "", "", ""]}
    dinnerDict = {"11-11-1911": ["", "", "", "", "", "", "", ""]}
    lunchDict = {"11-11-1911": ["", "", "", "", "", "", "", ""]}
    breakDict = {"11-11-1911": ["", "", "", "", "", "", "", ""]}
    if smeals != None:
        for row in smeals:
            i = 0
            y = 0

            key = ""
            for entry in row:

                if i == 1:
                    key = str(entry)
                    snackDict[key] = ["", "", "", "", "", "", "", ""]
                elif i>2:
                    if not str(entry).startswith("initialized food item") :
                        snackDict[key][y] = str(entry)
                    y+=1
                i+=1
    cur.execute("SELECT * FROM dmeals WHERE USERNAME = %s", (username,))
    conn.commit()
    dmeals = cur.fetchall()
    if dmeals != None:
        for row in dmeals:
            i = 0
            y = 0

            key = ""
            for entry in row:

                if i == 1:
                    key = str(entry)
                    dinnerDict[key] = ["", "", "", "", "", "", "", ""]
                elif i>2:
                    if not str(entry).startswith("initialized food item") :
                        dinnerDict[key][y] = str(entry)
                    y+=1
                i+=1
    cur.execute("SELECT * FROM lmeals WHERE USERNAME = %s", (username,))
    conn.commit()
    lmeals = cur.fetchall()
    if lmeals != None:
        for row in lmeals:
            i = 0
            y = 0

            key = ""
            for entry in row:

                if i == 1:
                    key = str(entry)
                    lunchDict[key] = ["", "", "", "", "", "", "", ""]
                elif i>2:
                    if not str(entry).startswith("initialized food item") :
                        lunchDict[key][y] = str(entry)
                    y+=1
                i+=1
    cur.execute("SELECT * FROM bmeals WHERE USERNAME = %s", (username,))
    conn.commit()
    bmeals = cur.fetchall()
    if bmeals != None:
        for row in bmeals:
            i = 0
            y = 0

            key = ""
            for entry in row:

                if i == 1:
                    key = str(entry)
                    breakDict[key] = ["", "", "", "", "", "", "", ""]
                elif i>2:
                    if not str(entry).startswith("initialized food item") :
                        breakDict[key][y] = str(entry)
                    y+=1
                i+=1
    return {"meals": [breakDict, lunchDict, dinnerDict, snackDict]}


@app.route('/doWork/<aThing>', methods=['GET', 'POST'])
def getTheMeals(aThing):
    if 'username' in session:
        if request.method == 'POST':
            if aThing == "getMeals":
                return jsonify(getAllMeals())

def recommendCals(user):
    #feet, inches, weight, age, gender(0-male, 1-female, 2-other), activity(1-little,2-light,3-moderate,4-very active,5-extra active)
    #cur.execute("CREATE TABLE IF NOT EXISTS users (username varchar, password varchar, feet int, inches int, weight int, age int, gender int, activity, int)")
    age=0
    gender=2
    act=0
    weight=0
    feet=0
    inch=0
    bmr=0
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE USERNAME = %s", (user,))
    conn.commit()
    entries = cur.fetchall()[0]
    print(entries)
    conn.close()
    if entries == None or entries == [] or entries == set():
        return -1
    else:
        age=entries[5]
        gender=entries[6]
        act=entries[7]
        weight=entries[4]
        feet=entries[2]
        inch=entries[3]
        totH=((feet*12)+inch)*2.54
        if gender == 0:
            #for men...
            #BMR = 66 + (13.7 x weight in kilos) + (5 x height in cm) – (6.8 x age in years)
            bmr = 66 + (13.7 * (weight / 2.2)) + (5 * totH) - (6.8 * age)
        else:
            #for women, or other...
            #BMR = 655 + (9.6 X weight in kilos) + (1.8 X height in cm) – (4.7 x age in years).
            bmr = 655 + (9.6 * (weight / 2.2)) + (1.8 * totH) - (4.7 * age)

        if act == 1:
            return {"Rec":(1.2 * bmr)}
        elif act == 2:
            return {"Rec":(1.375 * bmr)}
        elif act == 3:
            return {"Rec":(1.55 * bmr)}
        elif act == 4:
            return {"Rec":(1.725 * bmr)}
        elif act == 5:
            return {"Rec":(1.9 * bmr)}



@app.route('/calendar', methods=['GET', 'POST'])
def calendar():
    if 'username' in session:
        if request.method == 'GET':
            return render_template("calendar.html")
        elif request.method == 'POST':
            return jsonify( recommendCals(session['username']) )
        else:
            abort(404)
            return 'Never returned'
    else:
        abort(404)
        return 'Never returned'


@app.route('/calendar.js')
def calenOne():
    return render_template("calendar.js")

@app.route('/calendar.css')
def calenTwo():
    return render_template("calendar.css")

''' start of Jake's stuff '''

def createJSON(username):
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("SELECT LOGINS FROM ACHS WHERE USERNAME = %s ", (username,))
    conn.commit()
    logins = cur.fetchone()[0]
    print("GOT THE LOGINS" + str(logins) + "\n")
    cur.execute("SELECT MEALSMADE FROM ACHS WHERE USERNAME = %s ", (username,))
    conn.commit()
    mealsMade = cur.fetchone()[0]
    print("GOT THE MEALS " + str(mealsMade) + "\n")
    conn.close()
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


@app.route('/achievements', methods=['GET', 'POST'])
def userAchievements():
    username = session['username']
    if 'username' in session and session['username'] == username:
        if (request.method == 'POST'):
            return jsonify(createJSON(username))
        elif (request.method == 'GET'):
            return render_template("achievements.html")

@app.route("/achievements.css")
def achOne():
    return render_template("achievements.css")

@app.route("/achievements.js")
def achTwo():
    return render_template("achievements.js")


''' End of Jakes stuff '''




#updates bfast database
def bData(name, date):
    username = session['username']
    #determine if there exists an entry for this date yet
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("SELECT (EXISTS (SELECT * FROM bmeals WHERE USERNAME = %s AND DATE = %s))", (username, date))
    conn.commit()
    exists = cur.fetchone()[0]
    print("exists is equal to : " + str(exists))
    #if there is an entry for that username and date, then...
    if bool(exists) :
        #continue
        #!!!!!!!!!!!!!!!!! make sure you set bmeals to zero in initialize db
        cur.execute("SELECT NOMEALS FROM bmeals WHERE USERNAME = %s AND DATE = %s", (username, date))
        conn.commit()
        bmeals = cur.fetchone()[0]
        #print("GOT THE LOGINS" + str(logins) + "\n")
        #this tells us what slot we should put the food in
        #functionality to find next food slot
        cur.execute("SELECT * FROM bmeals WHERE USERNAME = %s AND DATE = %s", (username, date))
        conn.commit()
        dbEntries = cur.fetchone()
        i=0
        mNo=-1
        emptyNotFound = True
        foodSlot=""
        for entry in dbEntries:
            if i>2:
                if entry.startswith("initialized food item") and emptyNotFound:
                    mNo=i-2
                    emptyNotFound = False
            i+=1
        if emptyNotFound:
            #then we can just go off of NOMEALS
            if ( (bmeals+1) < 9):
                foodSlot = "M" + str(bmeals + 1)
            else:
                foodSlot = "M1"
                cur.execute("UPDATE bmeals SET NOMEALS = 0 WHERE USERNAME = %s AND DATE = %s", (username, date))
        else:
            #set NOMEALS to mNo
            foodSlot = "M" + str(mNo)
        #end of functionality to find next food slot
        #foodSlot, name, username
        sql = "UPDATE bmeals SET "+foodSlot+" = %s WHERE USERNAME = %s AND DATE = %s"
        cur.execute(sql, (name, username, date))
        conn.commit()
        #if no empty slot was found, increment nomeals so we know what value to replace
        if emptyNotFound:
            cur.execute("UPDATE bmeals SET NOMEALS = NOMEALS + 1 WHERE USERNAME = %s AND DATE = %s", (username, date))
            conn.commit()
        print("updating mealsMade\n")
        cur.execute("UPDATE ACHS SET MEALSMADE = MEALSMADE + 1 WHERE USERNAME = %s", (session['username'],))
        conn.commit()
        #for testing purposes
        cur.execute("SELECT * FROM bmeals WHERE USERNAME = %s AND DATE = %s", (username, date))
        conn.commit()
        bmeals = cur.fetchone()
        for elem in bmeals:
            print(elem)
        conn.close()
        return True
    #if there isn't an entry for that user and date yet, then...
    elif bool(exists) == False :
        print("EXISTS was false")
        strng = "initialized food item space                                                             "
        cur.execute("INSERT INTO bmeals(USERNAME, DATE, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, date, 0, strng, strng, strng, strng, strng, strng, strng, strng))
        conn.commit()
        foodSlot = "M1"
        #foodSlot, name, username
        sql = "UPDATE bmeals SET "+foodSlot+" = %s WHERE USERNAME = %s AND DATE = %s"
        cur.execute(sql, (name, username, date))
        conn.commit()
        cur.execute("UPDATE bmeals SET NOMEALS = NOMEALS + 1 WHERE USERNAME = %s AND DATE = %s", (username, date))
        print("updating mealsMade\n")
        cur.execute("UPDATE ACHS SET MEALSMADE = MEALSMADE + 1 WHERE USERNAME = %s", (session['username'],))
        conn.commit()
        #for testing purposes...
        cur.execute("SELECT * FROM bmeals WHERE USERNAME = %s  AND DATE = %s", (username, date))
        conn.commit()
        bmeals = cur.fetchone()
        for elem in bmeals:
            print(elem)
        conn.close()
        return True
    else:
        conn.close()
        print("SOMETHING WENT TERRIBLY WRONG")
        return False


def lData(name, date):
    username = session['username']
    #determine if there exists an entry for this date yet
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("SELECT (EXISTS (SELECT * FROM lmeals WHERE USERNAME = %s AND DATE = %s))", (username, date))
    conn.commit()
    exists = cur.fetchone()[0]
    print("exists is equal to : " + str(exists))
    #if there is an entry for that username and date, then...
    if bool(exists) :
        #continue
        #!!!!!!!!!!!!!!!!! make sure you set bmeals to zero in initialize db
        cur.execute("SELECT NOMEALS FROM lmeals WHERE USERNAME = %s AND DATE = %s", (username, date))
        conn.commit()
        lmeals = cur.fetchone()[0]
        #print("GOT THE LOGINS" + str(logins) + "\n")
        #this tells us what slot we should put the food in
        #functionality to find next food slot
        cur.execute("SELECT * FROM lmeals WHERE USERNAME = %s AND DATE = %s", (username, date))
        conn.commit()
        dbEntries = cur.fetchone()
        i=0
        mNo=-1
        emptyNotFound = True
        foodSlot=""
        for entry in dbEntries:
            if i>2:
                if entry.startswith("initialized food item") and emptyNotFound:
                    mNo=i-2
                    emptyNotFound = False
            i+=1
        if emptyNotFound:
            #then we can just go off of NOMEALS
            if ( (lmeals+1) < 9):
                foodSlot = "M" + str(lmeals + 1)
            else:
                foodSlot = "M1"
                cur.execute("UPDATE lmeals SET NOMEALS = 0 WHERE USERNAME = %s AND DATE = %s", (username, date))
        else:
            #set NOMEALS to mNo
            foodSlot = "M" + str(mNo)
        #end of functionality to find next food slot
        #foodSlot, name, username
        sql = "UPDATE lmeals SET "+foodSlot+" = %s WHERE USERNAME = %s AND DATE = %s"
        cur.execute(sql, (name, username, date))
        conn.commit()
        #if no empty slot was found, increment nomeals so we know what value to replace
        if emptyNotFound:
            cur.execute("UPDATE lmeals SET NOMEALS = NOMEALS + 1 WHERE USERNAME = %s AND DATE = %s", (username, date))
            conn.commit()
        print("updating mealsMade\n")
        cur.execute("UPDATE ACHS SET MEALSMADE = MEALSMADE + 1 WHERE USERNAME = %s", (session['username'],))
        conn.commit()
        #for testing purposes
        cur.execute("SELECT * FROM lmeals WHERE USERNAME = %s AND DATE = %s", (username, date))
        conn.commit()
        lmeals = cur.fetchone()
        for elem in lmeals:
            print(elem)
        conn.close()
        return True
    #if there isn't an entry for that user and date yet, then...
    elif bool(exists) == False :
        print("EXISTS was false")
        strng = "initialized food item space                                                             "
        cur.execute("INSERT INTO lmeals(USERNAME, DATE, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, date, 0, strng, strng, strng, strng, strng, strng, strng, strng))
        conn.commit()
        foodSlot = "M1"
        #foodSlot, name, username
        sql = "UPDATE lmeals SET "+foodSlot+" = %s WHERE USERNAME = %s AND DATE = %s"
        cur.execute(sql, (name, username, date))
        conn.commit()
        cur.execute("UPDATE lmeals SET NOMEALS = NOMEALS + 1 WHERE USERNAME = %s AND DATE = %s", (username, date))
        print("updating mealsMade\n")
        cur.execute("UPDATE ACHS SET MEALSMADE = MEALSMADE + 1 WHERE USERNAME = %s", (session['username'],))
        conn.commit()
        #for testing purposes...
        cur.execute("SELECT * FROM lmeals WHERE USERNAME = %s  AND DATE = %s", (username, date))
        conn.commit()
        lmeals = cur.fetchone()
        for elem in lmeals:
            print(elem)
        conn.close()
        return True
    else:
        conn.close()
        print("SOMETHING WENT TERRIBLY WRONG")
        return False


def dData(name, date):
    username = session['username']
    #determine if there exists an entry for this date yet
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("SELECT (EXISTS (SELECT * FROM dmeals WHERE USERNAME = %s AND DATE = %s))", (username, date))
    conn.commit()
    exists = cur.fetchone()[0]
    print("exists is equal to : " + str(exists))
    #if there is an entry for that username and date, then...
    if bool(exists) :
        #continue
        #!!!!!!!!!!!!!!!!! make sure you set bmeals to zero in initialize db
        cur.execute("SELECT NOMEALS FROM dmeals WHERE USERNAME = %s AND DATE = %s", (username, date))
        conn.commit()
        dmeals = cur.fetchone()[0]
        #print("GOT THE LOGINS" + str(logins) + "\n")
        #this tells us what slot we should put the food in
        #functionality to find next food slot
        cur.execute("SELECT * FROM dmeals WHERE USERNAME = %s AND DATE = %s", (username, date))
        conn.commit()
        dbEntries = cur.fetchone()
        i=0
        mNo=-1
        emptyNotFound = True
        foodSlot=""
        for entry in dbEntries:
            if i>2:
                if entry.startswith("initialized food item") and emptyNotFound:
                    mNo=i-2
                    emptyNotFound = False
            i+=1
        if emptyNotFound:
            #then we can just go off of NOMEALS
            if ( (dmeals+1) < 9):
                foodSlot = "M" + str(dmeals + 1)
            else:
                foodSlot = "M1"
                cur.execute("UPDATE dmeals SET NOMEALS = 0 WHERE USERNAME = %s AND DATE = %s", (username, date))
        else:
            #set NOMEALS to mNo
            foodSlot = "M" + str(mNo)
        #end of functionality to find next food slot
        #foodSlot, name, username
        sql = "UPDATE dmeals SET "+foodSlot+" = %s WHERE USERNAME = %s AND DATE = %s"
        cur.execute(sql, (name, username, date))
        conn.commit()
        #if no empty slot was found, increment nomeals so we know what value to replace
        if emptyNotFound:
            cur.execute("UPDATE dmeals SET NOMEALS = NOMEALS + 1 WHERE USERNAME = %s AND DATE = %s", (username, date))
            conn.commit()
        print("updating mealsMade\n")
        cur.execute("UPDATE ACHS SET MEALSMADE = MEALSMADE + 1 WHERE USERNAME = %s", (session['username'],))
        conn.commit()
        #for testing purposes
        cur.execute("SELECT * FROM bmeals WHERE USERNAME = %s AND DATE = %s", (username, date))
        conn.commit()
        dmeals = cur.fetchone()
        for elem in dmeals:
            print(elem)
        conn.close()
        return True
    #if there isn't an entry for that user and date yet, then...
    elif bool(exists) == False :
        print("EXISTS was false")
        strng = "initialized food item space                                                             "
        cur.execute("INSERT INTO dmeals(USERNAME, DATE, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, date, 0, strng, strng, strng, strng, strng, strng, strng, strng))
        conn.commit()
        foodSlot = "M1"
        #foodSlot, name, username
        sql = "UPDATE dmeals SET "+foodSlot+" = %s WHERE USERNAME = %s AND DATE = %s"
        cur.execute(sql, (name, username, date))
        conn.commit()
        cur.execute("UPDATE dmeals SET NOMEALS = NOMEALS + 1 WHERE USERNAME = %s AND DATE = %s", (username, date))
        print("updating mealsMade\n")
        cur.execute("UPDATE ACHS SET MEALSMADE = MEALSMADE + 1 WHERE USERNAME = %s", (session['username'],))
        conn.commit()
        #for testing purposes...
        cur.execute("SELECT * FROM dmeals WHERE USERNAME = %s  AND DATE = %s", (username, date))
        conn.commit()
        dmeals = cur.fetchone()
        for elem in dmeals:
            print(elem)
        conn.close()
        return True
    else:
        conn.close()
        print("SOMETHING WENT TERRIBLY WRONG")
        return False


def sData(name, date):
    username = session['username']
    #determine if there exists an entry for this date yet
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("SELECT (EXISTS (SELECT * FROM smeals WHERE USERNAME = %s AND DATE = %s))", (username, date))
    conn.commit()
    exists = cur.fetchone()[0]
    print("exists is equal to : " + str(exists))
    #if there is an entry for that username and date, then...
    if bool(exists) :
        #continue
        #!!!!!!!!!!!!!!!!! make sure you set bmeals to zero in initialize db
        cur.execute("SELECT NOMEALS FROM smeals WHERE USERNAME = %s AND DATE = %s", (username, date))
        conn.commit()
        smeals = cur.fetchone()[0]
        #print("GOT THE LOGINS" + str(logins) + "\n")
        #this tells us what slot we should put the food in
        #functionality to find next food slot
        cur.execute("SELECT * FROM smeals WHERE USERNAME = %s AND DATE = %s", (username, date))
        conn.commit()
        dbEntries = cur.fetchone()
        i=0
        mNo=-1
        emptyNotFound = True
        foodSlot=""
        for entry in dbEntries:
            if i>2:
                if entry.startswith("initialized food item") and emptyNotFound:
                    mNo=i-2
                    emptyNotFound = False
            i+=1
        if emptyNotFound:
            #then we can just go off of NOMEALS
            if ( (smeals+1) < 9):
                foodSlot = "M" + str(smeals + 1)
            else:
                foodSlot = "M1"
                cur.execute("UPDATE smeals SET NOMEALS = 0 WHERE USERNAME = %s AND DATE = %s", (username, date))
        else:
            #set NOMEALS to mNo
            foodSlot = "M" + str(mNo)
        #end of functionality to find next food slot
        #foodSlot, name, username
        sql = "UPDATE smeals SET "+foodSlot+" = %s WHERE USERNAME = %s AND DATE = %s"
        cur.execute(sql, (name, username, date))
        conn.commit()
        #if no empty slot was found, increment nomeals so we know what value to replace
        if emptyNotFound:
            cur.execute("UPDATE smeals SET NOMEALS = NOMEALS + 1 WHERE USERNAME = %s AND DATE = %s", (username, date))
            conn.commit()
        print("updating mealsMade\n")
        cur.execute("UPDATE ACHS SET MEALSMADE = MEALSMADE + 1 WHERE USERNAME = %s", (session['username'],))
        conn.commit()
        #for testing purposes
        cur.execute("SELECT * FROM smeals WHERE USERNAME = %s AND DATE = %s", (username, date))
        conn.commit()
        smeals = cur.fetchone()
        for elem in smeals:
            print(elem)
        conn.close()
        return True
    #if there isn't an entry for that user and date yet, then...
    elif bool(exists) == False :
        print("EXISTS was false")
        strng = "initialized food item space                                                             "
        cur.execute("INSERT INTO smeals(USERNAME, DATE, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, date, 0, strng, strng, strng, strng, strng, strng, strng, strng))
        conn.commit()
        foodSlot = "M1"
        #foodSlot, name, username
        sql = "UPDATE smeals SET "+foodSlot+" = %s WHERE USERNAME = %s AND DATE = %s"
        cur.execute(sql, (name, username, date))
        conn.commit()
        cur.execute("UPDATE smeals SET NOMEALS = NOMEALS + 1 WHERE USERNAME = %s AND DATE = %s", (username, date))
        print("updating mealsMade\n")
        cur.execute("UPDATE ACHS SET MEALSMADE = MEALSMADE + 1 WHERE USERNAME = %s", (session['username'],))
        conn.commit()
        #for testing purposes...
        cur.execute("SELECT * FROM smeals WHERE USERNAME = %s  AND DATE = %s", (username, date))
        conn.commit()
        bmeals = cur.fetchone()
        for elem in bmeals:
            print(elem)
        conn.close()
        return True
    else:
        conn.close()
        print("SOMETHING WENT TERRIBLY WRONG")
        return False


def pullBdata(date):
    print("we made it inside pullBData")


    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    username = session['username']
    cur.execute("SELECT * FROM bmeals WHERE USERNAME = %s AND DATE = %s", (username, date))
    conn.commit()
    bmeals = cur.fetchone()
    conn.close()
    returnJSON = {"1": [""],"2": [""],"3": [""],"4": [""],"5": [""],"6": [""],"7": [""],"8": [""]}
    i = 0
    if bmeals != None:
        for elem in bmeals:
            #print("Element number "+str(i)+" of bmeals is : "+str(elem))
            if i > 2:
                if not str(elem).startswith("initialized food item") :
                    returnJSON[str(i-2)] = [str(elem)]
                    #print("put "+str(elem)+" as value for key :"+str(i-2))
            #else:
                #print("did not append "+str(elem) +" to key "+str(i-2))
            i+=1
    print(returnJSON)
    return returnJSON


def pullLdata(date):
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    username = session['username']
    cur.execute("SELECT * FROM lmeals WHERE USERNAME = %s  AND DATE = %s", (username, date))
    conn.commit()
    lmeals = cur.fetchone()
    conn.close()
    returnJSON = {"1": [""],"2": [""],"3": [""],"4": [""],"5": [""],"6": [""],"7": [""],"8": [""]}
    i = 0
    if lmeals != None:
        for elem in lmeals:
            if i > 2:
                if not str(elem).startswith("initialized food item") :
                    returnJSON[str(i-2)] = [str(elem)]
            i+=1
    return returnJSON

def pullDdata(date):
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    username = session['username']
    cur.execute("SELECT * FROM dmeals WHERE USERNAME = %s  AND DATE = %s", (username, date))
    conn.commit()
    dmeals = cur.fetchone()
    conn.close()
    returnJSON = {"1": [""],"2": [""],"3": [""],"4": [""],"5": [""],"6": [""],"7": [""],"8": [""]}
    i = 0
    if dmeals != None:
        for elem in dmeals:
            if i > 2:
                if not str(elem).startswith("initialized food item") :
                    returnJSON[str(i-2)] = [str(elem)]
            i+=1
    return returnJSON

def pullSdata(date):
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    username = session['username']
    cur.execute("SELECT * FROM smeals WHERE USERNAME = %s AND DATE = %s", (username, date))
    conn.commit()
    smeals = cur.fetchone()
    conn.close()
    returnJSON = {"1": [""],"2": [""],"3": [""],"4": [""],"5": [""],"6": [""],"7": [""],"8": [""]}
    i = 0
    if smeals != None:
        for elem in smeals:
            if i > 2:
                if not str(elem).startswith("initialized food item") :
                    returnJSON[str(i-2)] = [str(elem)]
            i+=1
    return returnJSON




def connectAPI(nameOne):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=dhIFeY8WhF9o0tUGenudfxO0tAQEvByUb3N9bGIj&dataType=Survey%20(FNDDS)&query=" + nameOne.replace(" ", "%20")
    x = urllib.request.urlopen(url)
    #print(x)
    stuff = json.load(x)
    #print(stuff)
    if stuff.get("totalHits") != 0:
        foodsarray = stuff.get("foods")
        food = foodsarray[0]
        name = food.get("description")
        nutrient = food.get("foodNutrients")
        protein = nutrient[0]
        fat= nutrient[1]
        carbs = nutrient[2]
        calories= nutrient[3]
        astr = name+"   |   "+str(calories.get("value")) + " calories  |   " +str(carbs.get("value"))+" grams   |   " + str(fat.get("value"))+" grams   |   "+str(protein.get("value")) + " grams"
        print(astr)
        return astr
    else:
        return name

    # this will call the API and return a json
    #return {"food": "got from server"}

def removeEntry(Entry, theMeal, date):
    responseJSON = ""
    if theMeal == "b":
        conn = psycopg2.connect(db_config)
        cur = conn.cursor()
        username = session['username']
        st = "initialized food item space                                                             "
        cur.execute("UPDATE bmeals SET "+Entry+ " = %s WHERE USERNAME = %s AND DATE = %s", (st, username, date))
        conn.commit()
        conn.close()
        responseJSON = pullBdata(date)

    if theMeal == "l":
        conn = psycopg2.connect(db_config)
        cur = conn.cursor()
        username = session['username']
        st = "initialized food item space                                                             "
        cur.execute("UPDATE lmeals SET "+Entry+ " = %s WHERE USERNAME = %s AND DATE = %s", (st, username, date))
        conn.commit()
        conn.close()
        responseJSON = pullLdata(date)

    if theMeal == "d":
        conn = psycopg2.connect(db_config)
        cur = conn.cursor()
        username = session['username']
        st = "initialized food item space                                                             "
        cur.execute("UPDATE dmeals SET "+Entry+ " = %s WHERE USERNAME = %s AND DATE = %s", (st, username, date))
        conn.commit()
        conn.close()
        responseJSON = pullDdata(date)

    if theMeal == "s":
        conn = psycopg2.connect(db_config)
        cur = conn.cursor()
        username = session['username']
        st = "initialized food item space                                                             "
        cur.execute("UPDATE smeals SET "+Entry+ " = %s WHERE USERNAME = %s AND DATE = %s", (st, username, date))
        conn.commit()
        conn.close()
        responseJSON = pullSdata(date)
    return responseJSON




@app.route('/mealspage.js')
def mOne():
    return render_template("mealspage.js")


@app.route('/mealspage/<date>', methods = ['GET', 'POST'])
def mealspage(date):
    print("Got a meals request!\n")
    #date will come in the form "[month]-[day]-[year]"
    #example: "11-5-2021"
    if 'username' in session:
        if request.method == 'GET':
            # MAYBE CHECK IF "-" IS IN THERE FIRST SO WE DON'T GET POTENTIAL ERRORS?
            dateArray = date.split("-")
            month = dateArray[0]
            day = dateArray[1]
            year = dateArray[2]
            # now that we have date infomation, we can read from our template mealspage.txt and split at the desired responseText
            # at the split, we have to add a script that changes a js variable to "mealspage/<date>"
            theHTML = ""
            with open("mealspage.txt", "r") as f:
                theHTML = f.read()
                f.close()
            # MAYBE CHECK IF @@ IS IN THERE FIRST SO WE DON'T GET POTENTIAL ERRORS?
            htmlArray = theHTML.split("@@")
            injection = "<script>setPath('/mealspage/" + str(month) +"-"+ str(day) +"-"+ str(year) + "');</script>"
            return htmlArray[0] + injection + htmlArray[1]
            #return render_template('mealspage2.html')

        elif request.method == 'POST':

            dateArray = date.split("-")
            month = dateArray[0]
            day = dateArray[1]
            year = dateArray[2]


            print("It's a post request!\n")
            food = request.form["name"]
            print("The data is : " + food)


            if food.startswith("b") :
                food = food.split("b", maxsplit=1)[1]
                #create a response by connecting to the api with the food name
                theFood = connectAPI(food)
                #update the database to include our food
                bData(theFood, date)
                #create a responseJSON containing everything for breakfast
                responseJSON = pullBdata(date)
                print(responseJSON)
                return jsonify(responseJSON)

            elif food.startswith("l") :
                print("its lunch post request")
                food = food.split("l", maxsplit=1)[1]
                #create a response by connecting to the api with the food name
                #responseJSON = connectAPI(food)
                #update the database to include our food
                theFood = connectAPI(food)
                #update the database to include our food
                lData(theFood, date)

                #create a responseJSON containing everything for breakfast
                print("calling pullLData")
                responseJSON = pullLdata(date)
                print(responseJSON)
                return jsonify(responseJSON)
            elif food.startswith("d") :
                food = food.split("d", maxsplit=1)[1]
                #create a response by connecting to the api with the food name
                #responseJSON = connectAPI(food)
                theFood = connectAPI(food)
                #update the database to include our food
                dData(theFood, date)

                #create a responseJSON containing everything for breakfast
                responseJSON = pullDdata(date)
                print(responseJSON)
                return jsonify(responseJSON)
            elif food.startswith("s") :
                food = food.split("s", maxsplit=1)[1]
                #create a response by connecting to the api with the food name
                #responseJSON = connectAPI(food)
                theFood = connectAPI(food)
                #update the database to include our food
                sData(theFood, date)

                #create a responseJSON containing everything for breakfast
                responseJSON = pullSdata(date)
                print(responseJSON)
                return jsonify(responseJSON)
            elif food.startswith("zb") :
                print("we SHOULD BE IN HERE")
                responseJSON = pullBdata(date)
                return jsonify(responseJSON)
            elif food.startswith("zl") :
                responseJSON = pullLdata(date)
                return jsonify(responseJSON)
            elif food.startswith("zd") :
                responseJSON = pullDdata(date)
                return jsonify(responseJSON)
            elif food.startswith("zs") :
                responseJSON = pullSdata(date)
                return jsonify(responseJSON)




            elif food.startswith("1"):
                theMeal = food.split("1", maxsplit=1)[1]
                Entry = "M1"
                return jsonify(removeEntry(Entry, theMeal, date))

            elif food.startswith("2"):
                theMeal = food.split("2", maxsplit=1)[1]
                Entry = "M2"
                return jsonify(removeEntry(Entry, theMeal, date))
            elif food.startswith("3"):
                theMeal = food.split("3", maxsplit=1)[1]
                Entry = "M3"
                return jsonify(removeEntry(Entry, theMeal, date))
            elif food.startswith("4"):
                theMeal = food.split("4", maxsplit=1)[1]
                Entry = "M4"
                return jsonify(removeEntry(Entry, theMeal, date))
            elif food.startswith("5"):
                theMeal = food.split("5", maxsplit=1)[1]
                Entry = "M5"
                return jsonify(removeEntry(Entry, theMeal, date))
            elif food.startswith("6"):
                theMeal = food.split("6", maxsplit=1)[1]
                Entry = "M6"
                return jsonify(removeEntry(Entry, theMeal, date))
            elif food.startswith("7"):
                theMeal = food.split("7", maxsplit=1)[1]
                Entry = "M7"
                return jsonify(removeEntry(Entry, theMeal, date))
            elif food.startswith("8"):
                theMeal = food.split("8", maxsplit=1)[1]
                Entry = "M8"
                return jsonify(removeEntry(Entry, theMeal, date))


            else:
                print("we didn't get any of them")
                abort(404)
                return 'Never returned'
                #return jsonify({})#then send a json with all of the foods stored

    else:
        abort(404)
        return 'Never returned'

def get_user(username):
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("SELECT feet, inches, weight, age, gender, activity FROM users WHERE username=%s", (username, ))
    user = cur.fetchone()
    return user


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
        elif type_ == "age":
            update_age(username, request.form["age"])
        elif type_ == "gender":
            update_gender(username, request.form["gender"])
        elif type_ == "activity":
            update_activity(username, request.form["activity"])
        elif type_ == "delete":
            if not delete_user(username, request.form['current_pw']):
                return render_template("profile.html")
            return render_template("index.html")
        else:
            pass
    elif request.method == "DELETE":
        if not delete_user(username, request.form['current_pw']):
            return render_template("profile.html")
        return render_template("index.html")

    user = get_user(username)
    if user != None:
        return render_template("profile.html", user={"username": username,"feet": user[0], "inches": user[1], "pounds": user[2], "age": user[3], "gender": user[4], "activity": user[5]})
    else:
        print(f"Could NOT Find User: {username}")
        return render_template("profile.html")


def delete_user(username, password):
    if not verify_login(username, password):
        return False
    #conn = psycopg2.connect(db_config, sslmode="require")
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    hashkey = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), bytes(username, 'utf-8'), 100000).hex()
    cur.execute("DELETE FROM users where username=%s AND password=%s", (username, hashkey))
    conn.commit()
    conn.close()
    return True

def update_height(username, feet, inches):
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("UPDATE users SET feet=%s, inches=%s WHERE username=%s", (feet, inches, username))
    conn.commit()
    conn.close()

def update_weight(username, weight):
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("UPDATE users SET weight=%s WHERE username=%s", (weight, username))
    conn.commit()
    conn.close()

def update_age(username, age):
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("UPDATE users SET age=%s WHERE username=%s", (age, username))
    conn.commit()
    conn.close()

def update_gender(username, gender):
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("UPDATE users SET gender=%s WHERE username=%s", (gender, username))
    conn.commit()
    conn.close()

def update_activity(username, activity):
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("UPDATE users SET activity=%s WHERE username=%s", (activity, username))
    conn.commit()
    conn.close()

def update_password(username, current, new):
    if not verify_login(username, current):
        return
    hashkey = hashlib.pbkdf2_hmac('sha256', bytes(new, 'utf-8'), bytes(username, 'utf-8'), 100000).hex()
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    cur.execute("UPDATE users SET password=%s WHERE username=%s", (hashkey, username))
    conn.commit()
    conn.close()

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

@app.route('/recipes/<date>', methods=["GET", "POST"])
def recipe_page(date):
    if date is None:
        abort(404)
    if 'username' in session and verify_user(session['username']):
        if request.method == 'POST':
            print(request.form.getlist("foods"))
            sys.stdout.flush()
            ingred = ""
            if len(request.form.getlist("foods")) == 0:
                output = "<p>No results Found :(</p>"
                toPrint = "<head><title>Search Results</title></head><body><h1>Recipe Suggestions</h1><br>" + output + "<a href='recipes'>Return to Recipes Page</a></body>"
                return toPrint
            for food in request.form.getlist("foods"):
                ingred = ingred + urllib.parse.quote_plus(food)
            #ingred = ingred[:-1] #chop off last comma
            print("opendb meal search")
            sys.stdout.flush()
            url = "https://www.themealdb.com/api/json/v1/1/filter.php?i=" + ingred
            x = urllib.request.urlopen(url)
            print(x)
            stuff = json.load(x)
            print(stuff)
            sys.stdout.flush()
            if stuff['meals'] is None:
                return render_template("recipe_results.html", recipes=None)
            ids = ""
            output = ""
            for meal in stuff['meals']:
                meal_id = meal["idMeal"]
                url = "https://www.themealdb.com/api/json/v1/1/lookup.php?i=" + meal_id
                x = urllib.request.urlopen(url)
                print(x)
                mealdets = json.load(x)
                print(mealdets)
                if mealdets["meals"] is None:
                    continue
                output = output+"<br><h2>" + mealdets["meals"][0]["strMeal"] + "</h2><br><p>" + mealdets["meals"][0]["strInstructions"]+"</p><br><br>"
            if output == "":
                output = "<p>No results Found :(</p><br>"
            print(output)
            sys.stdout.flush()
            toPrint = "<head><title>Search Results</title></head><body><h1>Recipe Suggestions</h1><br>" + output + "<a href='" + date + "'>Return to Recipes Page</a></body>"
            return toPrint
        elif request.method == 'GET':
            return render_template('recipes.html', date=date)
    abort(404)
    return ''

@app.route("/recipes.js")
def recone():
    return render_template("recipes.js")

if __name__=="__main__":
    setup = initialize_db()
    if setup:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
        print(port)
        app.run(host="0.0.0.0",port=port)
