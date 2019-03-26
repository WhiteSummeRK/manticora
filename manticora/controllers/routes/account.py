from flask import (Flask, render_template, Blueprint,
                   request, url_for, redirect, abort, jsonify)
from flask_login import login_required, current_user

# modulos
from manticora.controllers.modules.account import (
    show_rests_accounts,
    query_account_and_build_html,
    show_clients_account,
    update_status_account,
    mount_user_data) #NOQA


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
    id_account = request.json.get('id_to_send')
    account = query_account_and_build_html(id_account)
    return jsonify({"result": account})


@app.route('/user_data/', methods=['POST'])
@login_required
def user_data():
    id_user = request.json.get('id_to_send')
    user = mount_user_data(id_user)

    return jsonify({"result": user})


@app.route('/adm_accounts/', methods=["GET"])
@login_required
def adm_accounts():
    accounts = show_clients_account(current_user)
    return render_template('adm_accounts.html', accounts=accounts)


@app.route('/adm_accounts/change_status/', methods=['POST'])
@login_required
def change_status():
    id_account = request.form.get('frente')

    new_status = update_status_account(id_account)

    return redirect(url_for('account.adm_accounts', upd=new_status))
