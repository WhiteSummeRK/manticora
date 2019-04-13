from flask import Flask, render_template, Blueprint, request

app = Blueprint('default_menus', __name__)


@app.route('/')
def login():
    return render_template('default_menus.html')
