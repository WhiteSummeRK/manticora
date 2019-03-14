from flask import Flask, render_template, Blueprint, request, url_for, redirect

# modulos
from manticora.controllers.modules.login import login
from flask_login import login_user

app = Blueprint('login', __name__)


@app.route('/',  methods=['GET'])
def login_template():
    return render_template('login.html')


@app.route('/',  methods=['POST'])
def login_view():
    data = request.form
    name = data['username']
    pwd = data['password']

    suposed_user = login(name, pwd)
    if suposed_user:
        login_user(suposed_user)
        return redirect(url_for('login.login_template'))
    return redirect(url_for('index.login', auth=False))
