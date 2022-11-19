from flask import Flask, request
from flask.templating import render_template

app = Flask(__name__, template_folder="static")

@app.get("/")
def home():
    return render_template('home.html')

@app.get("/login")
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)