import sys

from flask import Flask, send_from_directory, render_template

app = Flask(__name__)

@app.route('/')
def mealspage():
    return render_template('index.html')

if __name__=="__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8080
    print(port)
    app.run(host="0.0.0.0",port=port)
