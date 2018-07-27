from flask import Flask, render_template, Blueprint


app = Blueprint('login', __name__)


@app.route('/')
def login():
    return render_template('login.html')
