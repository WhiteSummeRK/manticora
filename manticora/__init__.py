"""Start flask app."""
from flask import Flask
from manticora.models.database.tables import db, db_url


app = Flask(__name__, template_folder='views', static_folder='assets')

from .controllers.routes.login import app as login  # NOQA
app.register_blueprint(login, url_prefix='/login')

from .controllers.routes.register import app as register  # NOQA
app.register_blueprint(register, url_prefix='/register')

from .controllers.routes.index import app as index  # NOQA
app.register_blueprint(index, url_prefix='/')

app.secret_key = b'\x89\x03\xf4\xdc\x1a\x95f\xe0\xae!\xf6Ml\xc6\x03\xc4'
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
