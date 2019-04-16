from flask import (Flask, render_template,
                   Blueprint, request,
                   redirect, url_for, abort)
from flask_login import login_required, current_user


from manticora.controllers.modules.default_menus import (
    insert_default_card,
    show_default_menus)


app = Blueprint('default_menus', __name__)


def only_adms():
    if not current_user.is_adm:
        return abort(400)


@app.route('/', methods=['GET'])
@login_required
def login():
    only_adms()
    menus = show_default_menus(current_user)
    return render_template('default_menus.html', card=menus)


@app.route('/new_item/', methods=['POST'])
@login_required
def insert_item():
    only_adms()
    dia = request.form.get('dia')
    tipo = request.form.get('tipo')
    item = request.form.get('item')
    preco = request.form.get('price')
    card = insert_default_card(dia, tipo, item, preco, current_user)

    return redirect(url_for('default_menus.login', status=card))
