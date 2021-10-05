from flask import Flask, render_template
import sys
import os

app = Flask(__name__)

@app.route("/")
def sample_page():
    return render_template("index.html")

@app.route("/dbtest")
def database_activity():
    import psycopg2
    db_config = os.environ["DATABASE_URL"] if "DATABASE_URL" in os.environ else "user=postgres password=password"

    conn = psycopg2.connect(db_config, sslmode='require')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS users (username varchar, name varchar);")
    cur.execute("INSERT INTO USERS (username, name) VALUES (%s, %s)", ("friendly", "green"))
    cur.execute("SELECT * FROM users;")
    data_from_db = cur.fetchone()
    str = ''
    for data in data_from_db:
        str += data
        str += ' '
    return"<p>"+"data from database: "+str+"</p>"
    

if __name__=="__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(port)
    app.run(host="0.0.0.0",port=port)
