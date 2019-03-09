from flask import Flask, render_template, Blueprint, request, url_for

# modulos
from manticora.controllers.modules.login import login

app = Blueprint('login', __name__)


@app.route('/',  methods=['GET'])
def login_template():
    return render_template('login.html')


@app.route('/',  methods=['POST'])
def login_view():
    data = request.form
    name = data['username']
    pwd = data['password']

    if login(name, pwd):
        return 'funcionou'
    # return redirect(url_for('login.login_template'))
    return 'não funcionou'
