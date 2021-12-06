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

recipe_api = ("https://api.spoonacular.com/recipes/findByIngredients?apiKey=" + os.environ["RECIPE_KEY"]) if "RECIPE_KEY" in os.environ else "Not a valid URL"
recipe_key_api = ("apiKey=" + os.environ["RECIPE_KEY"]) if "RECIPE_KEY" in os.environ else "Not a valid URL"

def create_account(username, password, feet, inches, weight):
    #conn = psycopg2.connect(db_config, sslmode='require')
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    hashkey = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), bytes(username, 'utf-8'), 100000)
    cur.execute("INSERT INTO users (username, password, feet, inches, weight) VALUES (%s, %s, %s, %s, %s)", (username, hashkey.hex(), feet, inches, weight))


    cur.execute("INSERT INTO ACHS(USERNAME, LOGINS, MEALSMADE, ACH1, ACH2, ACH3) VALUES (%s, 0, 0, 'no', 'no', 'no')", (username,))

    strng = "initialized food item space                                                             "
    cur.execute("INSERT INTO bmeals(USERNAME, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, 0, strng, strng, strng, strng, strng, strng, strng, strng))
    cur.execute("INSERT INTO lmeals(USERNAME, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, 0, strng, strng, strng, strng, strng, strng, strng, strng))
    cur.execute("INSERT INTO dmeals(USERNAME, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, 0, strng, strng, strng, strng, strng, strng, strng, strng))
    cur.execute("INSERT INTO smeals(USERNAME, NOMEALS, M1, M2, M3, M4, M5, M6, M7, M8) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", (username, 0, strng, strng, strng, strng, strng, strng, strng, strng))


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
    cur.execute("CREATE TABLE IF NOT EXISTS users (username varchar, password varchar, feet int, inches int, weight int)")

    #cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ("Jake", "password"))

    #cur.execute("DROP TABLE IF EXISTS ACHS")
    sql ="CREATE TABLE IF NOT EXISTS ACHS(USERNAME VARCHAR PRIMARY KEY, LOGINS INT, MEALSMADE INT, ACH1 BOOLEAN NOT NULL, ACH2 BOOLEAN NOT NULL, ACH3 BOOLEAN NOT NULL)"
    cur.execute(sql)
    #cur.execute("INSERT INTO ACHS(USERNAME, LOGINS, MEALSMADE, ACH1, ACH2, ACH3) VALUES ('Jake', 0, 0, 'no', 'no', 'no')")

    #cur.execute("DROP TABLE IF EXISTS bmeals")
    #cur.execute("DROP TABLE IF EXISTS lmeals")
    #cur.execute("DROP TABLE IF EXISTS dmeals")
    #cur.execute("DROP TABLE IF EXISTS smeals")
    cur.execute("CREATE TABLE IF NOT EXISTS bmeals(USERNAME VARCHAR PRIMARY KEY, NOMEALS INT, M1 VARCHAR, M2 VARCHAR, M3 VARCHAR, M4 VARCHAR, M5 VARCHAR, M6 VARCHAR, M7 VARCHAR, M8 VARCHAR)")
    cur.execute("CREATE TABLE IF NOT EXISTS lmeals(USERNAME VARCHAR PRIMARY KEY, NOMEALS INT, M1 VARCHAR, M2 VARCHAR, M3 VARCHAR, M4 VARCHAR, M5 VARCHAR, M6 VARCHAR, M7 VARCHAR, M8 VARCHAR)")
    cur.execute("CREATE TABLE IF NOT EXISTS dmeals(USERNAME VARCHAR PRIMARY KEY, NOMEALS INT, M1 VARCHAR, M2 VARCHAR, M3 VARCHAR, M4 VARCHAR, M5 VARCHAR, M6 VARCHAR, M7 VARCHAR, M8 VARCHAR)")
    cur.execute("CREATE TABLE IF NOT EXISTS smeals(USERNAME VARCHAR PRIMARY KEY, NOMEALS INT, M1 VARCHAR, M2 VARCHAR, M3 VARCHAR, M4 VARCHAR, M5 VARCHAR, M6 VARCHAR, M7 VARCHAR, M8 VARCHAR)")


    conn.commit()




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
        return redirect(url_for("mealspage"))
        '''       !!!!!!   something happens here...     !!!!!!!!!!     '''

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
def bData(name):
    username = session['username']

    conn = psycopg2.connect(db_config)
    cur = conn.cursor()

    #!!!!!!!!!!!!!!!!! make sure you set bmeals to zero in initialize db
    cur.execute("SELECT NOMEALS FROM bmeals WHERE USERNAME = %s ", (username,))
    conn.commit()
    bmeals = cur.fetchone()[0]
    #print("GOT THE LOGINS" + str(logins) + "\n")

    #this tells us what slot we should put the food in
    foodSlot = ""
    if ( (bmeals+1) < 9):
        foodSlot = "M" + str(bmeals + 1)
    else:
        foodSlot = "M1"
        cur.execute("UPDATE bmeals SET NOMEALS = 0 WHERE USERNAME = %s", (username,))
    #foodSlot, name, username
    sql = "UPDATE bmeals SET "+foodSlot+" = %s WHERE USERNAME = %s"
    cur.execute(sql, (name, username))
    conn.commit()
    cur.execute("UPDATE bmeals SET NOMEALS = NOMEALS + 1 WHERE USERNAME = %s", (username,))
    print("updating mealsMade\n")
    cur.execute("UPDATE ACHS SET MEALSMADE = MEALSMADE + 1 WHERE USERNAME = %s", (session['username'],))

    conn.commit()


    cur.execute("SELECT * FROM bmeals WHERE USERNAME = %s ", (username,))
    conn.commit()
    bmeals = cur.fetchone()
    for elem in bmeals:
        print(elem)



    conn.close()
    return True

#pulls data for breakfast under the specified username and returns the meals in a list
#def pullBdata()

def lData(name):
    username = session['username']

    conn = psycopg2.connect(db_config)
    cur = conn.cursor()

    #!!!!!!!!!!!!!!!!! make sure you set bmeals to zero in initialize db
    cur.execute("SELECT NOMEALS FROM lmeals WHERE USERNAME = %s ", (username,))
    conn.commit()
    lmeals = cur.fetchone()[0]
    #print("GOT THE LOGINS" + str(logins) + "\n")

    #this tells us what slot we should put the food in
    foodSlot = ""
    if ( (lmeals+1) < 9):
        foodSlot = "M" + str(lmeals + 1)
    else:
        foodSlot = "M1"
        cur.execute("UPDATE lmeals SET NOMEALS = 0 WHERE USERNAME = %s", (username,))
    #foodSlot, name, username
    sql = "UPDATE lmeals SET "+foodSlot+" = %s WHERE USERNAME = %s"
    cur.execute(sql, (name, username))
    conn.commit()
    cur.execute("UPDATE lmeals SET NOMEALS = NOMEALS + 1 WHERE USERNAME = %s", (username,))
    print("updating mealsMade\n")
    cur.execute("UPDATE ACHS SET MEALSMADE = MEALSMADE + 1 WHERE USERNAME = %s", (session['username'],))

    conn.commit()

    cur.execute("SELECT * FROM lmeals WHERE USERNAME = %s ", (username,))
    conn.commit()
    lmeals = cur.fetchone()
    for elem in lmeals:
        print(elem)

    conn.close()
    return True

def dData(name):
    username = session['username']

    conn = psycopg2.connect(db_config)
    cur = conn.cursor()

    #!!!!!!!!!!!!!!!!! make sure you set bmeals to zero in initialize db
    cur.execute("SELECT NOMEALS FROM dmeals WHERE USERNAME = %s ", (username,))
    conn.commit()
    dmeals = cur.fetchone()[0]
    #print("GOT THE LOGINS" + str(logins) + "\n")

    #this tells us what slot we should put the food in
    foodSlot = ""
    if ( (dmeals+1) < 9):
        foodSlot = "M" + str(dmeals + 1)
    else:
        foodSlot = "M1"
        cur.execute("UPDATE dmeals SET NOMEALS = 0 WHERE USERNAME = %s", (username,))
    #foodSlot, name, username
    sql = "UPDATE dmeals SET "+foodSlot+" = %s WHERE USERNAME = %s"
    cur.execute(sql, (name, username))
    conn.commit()
    cur.execute("UPDATE dmeals SET NOMEALS = NOMEALS + 1 WHERE USERNAME = %s", (username,))
    print("updating mealsMade\n")
    cur.execute("UPDATE ACHS SET MEALSMADE = MEALSMADE + 1 WHERE USERNAME = %s", (session['username'],))

    conn.commit()

    cur.execute("SELECT * FROM dmeals WHERE USERNAME = %s ", (username,))
    conn.commit()
    dmeals = cur.fetchone()
    for elem in dmeals:
        print(elem)

    conn.close()
    return True

def sData(name):
    username = session['username']

    conn = psycopg2.connect(db_config)
    cur = conn.cursor()

    #!!!!!!!!!!!!!!!!! make sure you set bmeals to zero in initialize db
    cur.execute("SELECT NOMEALS FROM smeals WHERE USERNAME = %s ", (username,))
    conn.commit()
    smeals = cur.fetchone()[0]
    #print("GOT THE LOGINS" + str(logins) + "\n")

    #this tells us what slot we should put the food in
    foodSlot = ""
    if ( (smeals+1) < 9):
        foodSlot = "M" + str(smeals + 1)
    else:
        foodSlot = "M1"
        cur.execute("UPDATE smeals SET NOMEALS = 0 WHERE USERNAME = %s", (username,))
    #foodSlot, name, username
    sql = "UPDATE smeals SET "+foodSlot+" = %s WHERE USERNAME = %s"
    cur.execute(sql, (name, username))
    conn.commit()
    cur.execute("UPDATE smeals SET NOMEALS = NOMEALS + 1 WHERE USERNAME = %s", (username,))
    print("updating mealsMade\n")
    cur.execute("UPDATE ACHS SET MEALSMADE = MEALSMADE + 1 WHERE USERNAME = %s", (session['username'],))

    conn.commit()

    cur.execute("SELECT * FROM smeals WHERE USERNAME = %s ", (username,))
    conn.commit()
    smeals = cur.fetchone()
    for elem in smeals:
        print(elem)

    conn.close()
    return True

def pullBdata():
    print("we made it inside pullBData")
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    username = session['username']
    cur.execute("SELECT * FROM bmeals WHERE USERNAME = %s ", (username,))
    conn.commit()
    bmeals = cur.fetchone()
    conn.close()
    returnJSON = {"1": [""],"2": [""],"3": [""],"4": [""],"5": [""],"6": [""],"7": [""],"8": [""]}
    i = 0
    for elem in bmeals:
        if i > 1:
            if not str(elem).startswith("initialized food item") :
                returnJSON[str(i-1)] = [str(elem)]
        i+=1
    print(returnJSON)
    return returnJSON


def pullLdata():
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    username = session['username']
    cur.execute("SELECT * FROM lmeals WHERE USERNAME = %s ", (username,))
    conn.commit()
    lmeals = cur.fetchone()
    conn.close()
    returnJSON = {"1": [""],"2": [""],"3": [""],"4": [""],"5": [""],"6": [""],"7": [""],"8": [""]}
    i = 0
    for elem in lmeals:
        if i > 1:
            if not str(elem).startswith("initialized food item") :
                returnJSON[str(i-1)] = [str(elem)]
        i+=1
    return returnJSON

def pullDdata():
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    username = session['username']
    cur.execute("SELECT * FROM dmeals WHERE USERNAME = %s ", (username,))
    conn.commit()
    dmeals = cur.fetchone()
    conn.close()
    returnJSON = {"1": [""],"2": [""],"3": [""],"4": [""],"5": [""],"6": [""],"7": [""],"8": [""]}
    i = 0
    for elem in dmeals:
        if i > 1:
            if not str(elem).startswith("initialized food item") :
                returnJSON[str(i-1)] = [str(elem)]
        i+=1
    return returnJSON

def pullSdata():
    conn = psycopg2.connect(db_config)
    cur = conn.cursor()
    username = session['username']
    cur.execute("SELECT * FROM smeals WHERE USERNAME = %s ", (username,))
    conn.commit()
    smeals = cur.fetchone()
    conn.close()
    returnJSON = {"1": [""],"2": [""],"3": [""],"4": [""],"5": [""],"6": [""],"7": [""],"8": [""]}
    i = 0
    for elem in smeals:
        if i > 1:
            if not str(elem).startswith("initialized food item") :
                returnJSON[str(i-1)] = [str(elem)]
        i+=1
    return returnJSON

def connectAPI(nameOne):
    url = "https://api.nal.usda.gov/fdc/v1/foods/search?api_key=dhIFeY8WhF9o0tUGenudfxO0tAQEvByUb3N9bGIj&dataType=Survey%20(FNDDS)&query=" + nameOne
    x = urllib.request.urlopen(url)
    print(x)
    stuff = json.load(x)
    print(stuff)
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


@app.route('/mealspage.js')
def mOne():
    return render_template("mealspage.js")

@app.route('/mealspage', methods = ['GET', 'POST'])
def mealspage():
    print("Got a meals request!\n")
    if 'username' in session:
        if request.method == 'GET':
            return render_template('mealspage2.html')
        elif request.method == 'POST':
            print("It's a post request!\n")
            food = request.form["name"]
            print("The data is : " + food)


            if food.startswith("b") :
                food = food.split("b", maxsplit=1)[1]
                #create a response by connecting to the api with the food name
                theFood = connectAPI(food)
                #update the database to include our food
                bData(theFood)
                #create a responseJSON containing everything for breakfast
                responseJSON = pullBdata()
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
                lData(theFood)

                #create a responseJSON containing everything for breakfast
                print("calling pullLData")
                responseJSON = pullLdata()
                print(responseJSON)
                return jsonify(responseJSON)
            elif food.startswith("d") :
                food = food.split("d", maxsplit=1)[1]
                #create a response by connecting to the api with the food name
                #responseJSON = connectAPI(food)
                theFood = connectAPI(food)
                #update the database to include our food
                dData(theFood)

                #create a responseJSON containing everything for breakfast
                responseJSON = pullDdata()
                print(responseJSON)
                return jsonify(responseJSON)
            elif food.startswith("s") :
                food = food.split("s", maxsplit=1)[1]
                #create a response by connecting to the api with the food name
                #responseJSON = connectAPI(food)
                theFood = connectAPI(food)
                #update the database to include our food
                sData(theFood)

                #create a responseJSON containing everything for breakfast
                responseJSON = pullSdata()
                print(responseJSON)
                return jsonify(responseJSON)
            elif food.startswith("zb") :
                print("we SHOULD BE IN HERE")
                responseJSON = pullBdata()
                return jsonify(responseJSON)
            elif food.startswith("zl") :
                responseJSON = pullLdata()
                return jsonify(responseJSON)
            elif food.startswith("zd") :
                responseJSON = pullDdata()
                return jsonify(responseJSON)
            elif food.startswith("zs") :
                responseJSON = pullSdata()
                return jsonify(responseJSON)
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
    cur.execute("SELECT feet, inches, weight FROM users WHERE username=%s", (username, ))
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
        return render_template("profile.html", user={"username": username,"feet": user[0], "inches": user[1], "pounds": user[2]})
    else:
        print(f"Could NOT Find User: {username}")
        return render_template("profile.html")


def delete_user(username, password):
    if not verify_login(username, password):
        return False
    conn = psycopg2.connect(db_config, sslmode="require")
    cur = conn.cursor()
    hashkey = hashlib.pbkdf2_hmac('sha256', bytes(password, 'utf-8'), bytes(username, 'utf-8'), 100000).hex()
    cur.execute("DELETE FROM users where username=%s AND password=%s", (username, hashkey))
    conn.commit()
    conn.close()
    return True

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

@app.route('/recipes', methods=["GET", "POST"])
def recipe_page():
    if request.method == 'POST':
        request = recipe_api + "&number=2&ingreients="
        for food in request.form.getlist("food"):
            request = request + urllib.parse.quote_plus(food)+","
        request = request[:-1]
        print("spoon meal search")
        x = urllib.request.urlopen(request)
        print(x)
        stuff = json.load(x)
        print(stuff)
        if len(stuff) == 0:
            return render_template("recipe_results.html", recipes="<p>No results found :(</p>")
        url = "https://api.spoonacular.com/recipes/informationBulk?ids="
        for meal in stuff:
            meal_id = meal["id"]
            url = url + meal_id + ","
        url = url[:-1]#chop off extra comma
        url = url + "&" + recipe_api_key
        print("spoon recipe lookup")
        x = urllib.request.urlopen(request)
        print(x)
        stuff = json.load(x)
        print(stuff)
        output = ""
        for recipe in stuff:
            name = recipe['name']
            url = "none"
            if "sourceURL" in recipe:
                url = recipe['sourceURL']
            elif "spoonacularSourceURL" in recipe:
                url = recipe['spoonacularSourceURL']
            output = output + "<p>" + name + "</p>"
            output = output+"<br>"
            if url != "none":
                output = output+'<a href="'+url+'">Link to Recipe</a>'
                output = output+"<br>"
            output = output+"<br>"
        if output == "":
            output = "<p>No results Found :(</p>"
        return render_template("recipe_results.html", recipes=output)
    elif request.method == 'GET':
        return render_template('recipes.html')
    return ''

@app.route("/recipes.js")
def recone():
    return render_remplate("recipes.js")

#@app.route('/reciperesults', methods=["POST"])
#def get_recipes(recipes):
#return ''

#@app.route('/testloadmeals', methods=["GET", "POST"])
#def meal_selection_test():
#    if request.method == 'GET':
#        return render_template('selecttest.html')
#    elif request.method == 'POST':
#        return_string = "<p>Got from request: "
#        for food in request.form.getlist("foods"):
#            return_string = return_string + food + " "
#        return_string = return_string + "</p>"
#        return return_string
#    return ''

#@app.route('/testtexttoapi', methods=["GET", "POST"])
#def recipe_search_test():
#    if request.method == 'GET':
#        return render_template('texttest.html')
#    elif request.method == 'POST':
#        request = recipe_api + "&number=2&ingreients="
#        for food in request.form.getlist("food"):
#            request = request + urllib.parse.quote_plus(food)
#        print("spoon meal search")
#        x = urllib.request.urlopen(request)
#        print(x)
#        stuff = json.load(x)
#        print(stuff)
#        if len(stuff) == 0:
#            return "<p>No results found :(</p>"
#        url = "https://api.spoonacular.com/recipes/informationBulk?ids="
#        for meal in stuff:
#            meal_id = meal["id"]
#            url = url + meal_id + ","
#        url = url + "&" + recipe_api_key
#        print("spoon recipe lookup")
#        x = urllib.request.urlopen(request)
#        print(x)
#        stuff = json.load(x)
#        print(stuff)
#        output = ""
#        for recipe in stuff:
#            name = recipe['name']
#           url = "none"
#           if "sourceURL" in recipe:
#               url = recipe['sourceURL']
#            elif "spoonacularSourceURL" in recipe:
#               url = recipe['spoonacularSourceURL']
#            output = output + "<p>" + name + "</p>"
#           if url != "none":
#               output = output+'<a href="'+url+'">Link to Recipe</a>'
#            output = output+"<br>"
#        return output
#            
#    return ''

#@app.route('/selecttest.js')
#def testOne():
#    return render_template('selecttest.js')

if __name__=="__main__":
    setup = initialize_db()
    if setup:
        port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
        print(port)
        app.run(host="0.0.0.0",port=port)
