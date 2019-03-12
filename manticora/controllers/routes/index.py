from flask import Flask, render_template, Blueprint, request


app = Blueprint('index', __name__)


@app.route('/')
def login():
    return render_template('index.html')
