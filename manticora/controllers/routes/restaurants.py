from flask import (Flask, render_template, Blueprint,
                   request, url_for, redirect, abort, jsonify)
from flask_login import login_required, current_user

# modulos
from manticora.controllers.modules.restaurants import (show_restaurants,
                                                       show_all_citys,
                                                       show_rests_with_filter,
                                                       show_requests_to_rest,
                                                       update_status_request)
from manticora.controllers.modules.menu import (show_card_by_rest_id,
                                                register_user_request,
                                                update_bill)
from manticora.controllers.modules.register import (update_user,
                                                    update_rest,
                                                    update_rest_img)


app = Blueprint('restaurants', __name__)


def only_normal_users():
    if current_user.is_adm:
        return abort(400)


def only_adms():
    if not current_user.is_adm:
        return abort(400)


@app.route('/',  methods=['GET'])
@login_required
def login_template():
    only_normal_users()
    query_rest = request.args.get('search_rest')
    filter_box = request.args.get('filter_radio')
    citys = request.args.get('sel1')
    citys_ = show_all_citys()
    if filter_box:
        rests = show_rests_with_filter(filter_box, citys)
        return render_template('restaurants.html',
                               rests=rests,
                               citys=citys_)

    rests = show_restaurants(query_rest)
    return render_template('restaurants.html',
                           rests=rests,
                           citys=citys_)


@app.route('/',  methods=['POST'])
@login_required
def post_rests():
    only_normal_users()
    id_rest = request.json.get('id_to_send')
    card = show_card_by_rest_id(int(id_rest))
    return jsonify({"cardapio": card})


@app.route('/make_request/', methods=['POST'])
@login_required
def make_req():
    only_normal_users()
    rest_id = request.form.get('btn_req')
    foods = request.form.getlist('input_box')
    if not foods:
        return redirect(url_for('restaurants.login_template',
                                error="no item"))
    marmita_id = request.form.get('marmitas')
    user_account = update_bill(current_user, marmita_id, rest_id)
    register_user_request(marmita_id,
                          current_user,
                          rest_id,
                          foods)
    return redirect(url_for('restaurants.login_template',
                            conta="%.2f" % user_account.conta))


@app.route('/profile/', methods=['GET'])
@login_required
def adm_profile():
    only_adms()
    rest = show_restaurants(current_user.nome)[0]
    return render_template('adm_profile.html', rest=rest)


@app.route('/profile/addr/', methods=['POST'])
@login_required
def change_addr():
    only_adms()
    city = request.form.get('city_in')
    neigh = request.form.get('neigh_in')
    street = request.form.get('street_in')
    num = request.form.get('number_in')
    comp = request.form.get('comp_in')

    new_addr = update_user(city=city,
                           neigh=neigh,
                           street=street,
                           num=num,
                           complement=comp,
                           current_user=current_user)
    return redirect(url_for('restaurants.adm_profile', upd=new_addr))


@app.route('/profile/rest/', methods=['POST'])
@login_required
def change_rest():
    only_adms()
    phone = request.form.get('phone')
    hora_aber = request.form.get('hora_aber')
    hora_fech = request.form.get('hora_fech')

    new_rest = update_rest(phone, hora_aber, hora_fech, current_user)

    return redirect(url_for('restaurants.adm_profile', upd=new_rest))


@app.route('/profile/pic/', methods=['POST'])
@login_required
def change_pic():
    only_adms()
    imagem = request.files.get('img')
    new_img = update_rest_img(imagem, current_user)

    return redirect(url_for('restaurants.adm_profile', upd=new_img))


@app.route('/requests/', methods=["GET"])
@login_required
def requests_view():
    only_adms()
    requests = show_requests_to_rest(current_user)
    return render_template('requests.html', requests=requests)


@app.route('/requests/change_status/', methods=['POST'])
@login_required
def change_request_status():
    id_to_send = request.form.get('frente')
    new_status = update_status_request(id_to_send)

    return redirect(url_for('restaurants.requests_view', upd=new_status))
