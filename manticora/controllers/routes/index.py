from flask import Flask, render_template, Blueprint, request
from flask_login import logout_user

app = Blueprint('index', __name__)


@app.route('/')
def login():
    logout_user()
    return render_template('index.html')
