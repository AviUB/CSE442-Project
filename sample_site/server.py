from flask import Flask, render_template
import sys
import os

app = Flask(__name__)

@app.route("/")
def sample_page():
    return render_template("index.html")

@app.route("/create_account", methods=['GET','POST'])
def create_account_page():
    if request.method == 'POST':
        return create_account()
    else:
        return register_page()
    

if __name__=="__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(port)
    app.run(host="0.0.0.0",port=port)

def create_account():
    return"<p>"+"This is not finished"+"</p>"

def register_page():
    return"<p>"+"This is not finished"+"</p>"
