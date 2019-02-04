from flask import Flask, render_template, Blueprint, request, jsonify


app = Blueprint('register', __name__)


@app.route('/new_user/', methods=['POST'])
def new_user():
    return jsonify({'result': 'true'})


@app.route('/new_adm/', methods=['POST'])
def new_adm():
    return jsonify({'result': 'true'})
