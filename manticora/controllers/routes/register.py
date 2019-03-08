from flask import Flask, render_template, Blueprint, request, jsonify, request
from json import loads

# imports dos modulos
from manticora.controllers.modules.register import register_common_user

app = Blueprint('register', __name__)


@app.route('/new_user/', methods=['POST'])
def new_user():
    data = loads(request.data)
    name = data['name']
    email = data['email']
    pwd = data['pwd']

    return jsonify({
        'result': register_common_user(name, pwd, email, 'bairro1',
                                       'cidade1', 'rua1', 'numero1',
                                       'complemento')
    })


@app.route('/new_adm/', methods=['GET'])
def new_adm():
    return render_template('admin_register.html')
