from flask_script import Manager
from manticora import app

manager = Manager(app)


@manager.command
def runserver():
    app.run(debug=False)


if __name__ == "__main__":
    manager.run()
