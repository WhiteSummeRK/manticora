from flask import Flask, render_template, Blueprint, request

app = Blueprint('default_menus', __name__)


@app.route('/', methods=['GET'])
def login():
    return render_template('default_menus.html')


@app.route('/new_item/', methods=['POST'])
def insert_item():
    return render_template('default_menus.html')
