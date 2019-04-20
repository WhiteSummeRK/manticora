from json import loads
from flask import (render_template, Blueprint,
                   request, jsonify, redirect, url_for, abort)

# imports dos modulos
from manticora.controllers.modules.register import (register_user,
                                                    register_rest,
                                                    update_user)
from manticora.models.database.tables import db
from flask_login import current_user

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
        'result': register_user(name, pwd, email, neigh,
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
    open = request.form['hora_aber']
    closed = request.form['hora_fech']
    img = request.files['img']

    if open == closed:
        return redirect(url_for('register.new_adm',
                                new_adm='Desculpe, não é possivel utilizar um estabelecimento 24hrs')) # NOQA
    adm = register_user(name, pwd, email, neigh,
                        city, street, num_street,
                        comp, is_adm=True,
                        return_entity=True)

    if not type(adm) == str:
        rest = register_rest(phone, num_phone, img, open, closed, adm)
        return redirect(url_for('register.new_adm', new_adm=rest))
    return redirect(url_for('register.new_adm', new_adm=adm))


@app.route('/alter_user/', methods=['POST'])
def alter_user():
    data = request.form
    neigh = data.get('neigh_in')
    city = data.get('city_in')
    street = data.get('street_in')
    num = data.get('number_in')
    complement = data.get('comp_in')

    upd_user = update_user(city, neigh, street, num, complement, current_user)

    return redirect(url_for('login.login_template', upd=upd_user))
