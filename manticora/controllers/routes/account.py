from flask import (Flask, render_template, Blueprint,
                   request, url_for, redirect, abort, jsonify)
from flask_login import login_required, current_user

# modulos
from manticora.controllers.modules.account import (show_rests_accounts,
                                                   query_account_and_build_html) #NOQA

app = Blueprint('account', __name__)


def only_normal_users():
    if current_user.is_adm:
        return abort(400)


@app.route('/',  methods=['GET'])
@login_required
def account_index():
    only_normal_users()
    rests = show_rests_accounts(current_user)
    return render_template('account.html', rests=rests)


@app.route('/extrato/', methods=['POST'])
@login_required
def extrato_render():
    only_normal_users()
    id_account = request.json.get('id_to_send')
    account = query_account_and_build_html(id_account)
    return jsonify({"result": account})
