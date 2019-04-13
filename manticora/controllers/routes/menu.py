from flask import (Flask, render_template, Blueprint,
                   request, url_for, redirect, abort,
                   jsonify)

from flask_login import login_required, current_user

from manticora.controllers.modules.menu import (save_menu, show_menu_by_day,
                                                save_new_marmita,
                                                show_all_marmitas,
                                                del_item_from_menu,
                                                del_marm_size)

app = Blueprint('menu', __name__)


def only_adms():
    if not current_user.is_adm:
        return abort(400)


@app.route('/',  methods=['GET'])
@login_required
def menu_for_adm():
    only_adms()
    day = request.args.get('day')
    menu_items = show_menu_by_day(day, current_user)
    marmitas = show_all_marmitas(current_user)
    return render_template('menu.html', items=menu_items, marmitas=marmitas)


@app.route('/', methods=['POST'])
@login_required
def menu_post():
    only_adms()
    item = request.form.get('item')
    kind = request.form.get('type')
    day = request.form.get('day')
    preco_item = request.form.get('price')
    result = save_menu(item, kind, day, preco_item, current_user)
    return redirect(url_for('menu.menu_for_adm', insertion=result))


@app.route('/new_size/', methods=['POST'])
@login_required
def new_size_post():
    size = request.form.get('size')
    price = request.form.get('price').replace(',', '.')

    result = save_new_marmita(size, price, current_user)
    return redirect(url_for('menu.menu_for_adm', insertion=result))


@app.route('/delete_marm/', methods=['POST'])
@login_required
def del_marm():
    id_to_del = request.json.get('id_to_send')
    return jsonify({
        "result": del_marm_size(id_to_del)
        })

@app.route('/delete_item/', methods=['POST'])
@login_required
def del_item():
    id_to_del = request.json.get('id_to_send')
    return jsonify({
        "result": del_item_from_menu(id_to_del)
        })
