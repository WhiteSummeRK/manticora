from flask import Flask, render_template, Blueprint, request, jsonify, request
from json import loads

app = Blueprint('register', __name__)


@app.route('/new_user/', methods=['POST'])
def new_user():
    data = loads(request.data)
    name = data['name']
    email = data['email']
    pwd = data['pwd']

    return jsonify({'result': 'true'})


@app.route('/new_adm/', methods=['GET'])
def new_adm():
    return render_template('admin_register.html')
