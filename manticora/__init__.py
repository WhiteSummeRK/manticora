"""Start flask app."""
from flask import Flask
from manticora.models.database.tables import db, db_url, Usuario
from flask_login import LoginManager
from flask_session import Session

login_manager = LoginManager()
sess = Session()

app = Flask(__name__, template_folder='views', static_folder='assets')


from .controllers.routes.login import app as login  # NOQA
app.register_blueprint(login, url_prefix='/login')

from .controllers.routes.register import app as register  # NOQA
app.register_blueprint(register, url_prefix='/register')

from .controllers.routes.index import app as index  # NOQA
app.register_blueprint(index, url_prefix='/')

from .controllers.routes.restaurants import app as restaurants # NOQA
app.register_blueprint(restaurants, url_prefix='/restaurants')

from .controllers.routes.menu import app as menu # NOQA
app.register_blueprint(menu, url_prefix='/menu')

from .controllers.routes.account import app as account #NOQA
app.register_blueprint(account, url_prefix='/account')

app.secret_key = b'\x89\x03\xf4\xdc\x1a\x95f\xe0\xae!\xf6Ml\xc6\x03\xc4'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

sess.init_app(app)
login_manager.init_app(app)
db.init_app(app)


@login_manager.user_loader
def load_user(id):
    return Usuario.query.filter_by(id=ord(id)).first()
