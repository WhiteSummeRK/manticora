from flask_script import Manager
from manticora import app

manager = Manager(app)


@manager.command
def runserver():
    app.run(debug=True)


if __name__ == "__main__":
    manager.run()
