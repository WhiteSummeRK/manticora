from flask import Flask, render_template, Blueprint, request


app = Blueprint('', __name__)


@app.route('/')
def login():
    return render_template('index.html', new_adm="default")
