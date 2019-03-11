from json import loads
from flask import (render_template, Blueprint,
                   request, jsonify, redirect, url_for)

# imports dos modulos
from manticora.controllers.modules.register import (register_common_user,
                                                    register_adm)

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


@app.route('/new_adm/', methods=['POST'])
def new_adm_post():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    num_phone = request.form['num']
    pwd = request.form['pwd2']
    neigh = request.form['neigh']
    city = request.form['city']
    street = request.form['street']
    num_street = request.form['num_street']
    comp = request.form['comp']
    img = request.files['img']

    adm = register_adm(name, email, phone, num_phone, pwd, neigh, city,
                       street, num_street, comp, img)
    return "ok"
    # return redirect(url_for('login', new_adm=adm))
