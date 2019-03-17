from flask import (Flask, render_template, Blueprint,
                   request, url_for, redirect, abort)

# modulos
from manticora.controllers.modules.restaurants import (show_restaurants,
                                                       show_all_citys,
                                                       show_rests_with_filter)
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
