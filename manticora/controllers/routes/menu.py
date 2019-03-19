from flask import (Flask, render_template, Blueprint,
                   request, url_for, redirect, abort)

from flask_login import login_required, current_user

from manticora.controllers.modules.menu import (save_menu, show_menu_by_day)

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

    return render_template('menu.html', items=menu_items)


@app.route('/', methods=['POST'])
def menu_post():
    only_adms()
    item = request.form.get('item')
    kind = request.form.get('type')
    day = request.form.get('day')
    result = save_menu(item, kind, day, current_user)
    return redirect(url_for('menu.menu_for_adm', insertion=result))
