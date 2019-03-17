from flask import (Flask, render_template, Blueprint,
                   request, url_for, redirect, abort)

# modulos
from manticora.controllers.modules.restaurants import (show_restaurants,
                                                       show_all_citys)
from flask_login import login_required, current_user

app = Blueprint('restaurants', __name__)


def only_normal_users():
    if current_user.is_adm:
        return abort(400)


@app.route('/',  methods=['GET'])
@login_required
def login_template():
    only_normal_users()
    query_rest = request.args.get('search_rest')
    citys = show_all_citys()
    rests = show_restaurants(query_rest)

    return render_template('restaurants.html',
                           rests=rests,
                           citys=citys)


@app.route('/',  methods=['POST'])
def login_view():
    filter_box = request.form.get('filter_radio')
    city = request.form.get('sel1')
    return 'ok'
