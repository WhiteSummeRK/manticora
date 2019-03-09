from json import loads
from flask import render_template, Blueprint, request, jsonify

# imports dos modulos
from manticora.controllers.modules.register import register_common_user

app = Blueprint('register', __name__)


@app.route('/new_user/', methods=['POST'])
def new_user():
    data = loads(request.data)
    name = data['name']
    email = data['email']
    pwd = data['pwd']
    neigh = data['neigh']
    city = data['city']
    street = data['street']
    num = data['num']
    complement = data['complement']

    return jsonify({
        'result': register_common_user(name, pwd, email, neigh,
                                       city, street, num,
                                       complement)
    })


@app.route('/new_adm/', methods=['GET'])
def new_adm():
    return render_template('admin_register.html')
