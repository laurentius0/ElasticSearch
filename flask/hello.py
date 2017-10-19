from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    request.form['password']
    return "Hello World!"
