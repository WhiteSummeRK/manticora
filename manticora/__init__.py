"""Start flask app."""
from flask import Flask
from .controllers.routes.login import app as login  # NOQA

app = Flask(__name__, template_folder='views')

app.register_blueprint(login, url_prefix='/login')
