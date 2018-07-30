"""Start flask app."""
from flask import Flask
from .controllers.routes.login import app as login  # NOQA
from .controllers.routes.index import app as index  # NOQA


app = Flask(__name__, template_folder='views', static_folder='assets')

app.register_blueprint(login, url_prefix='/login')
app.register_blueprint(index, url_prefix='/')
