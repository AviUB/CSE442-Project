from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def sample_page():
    return render_template("index.html")

if __name__=="main":
    app.run(host="0.0.0.0",port=8080)
