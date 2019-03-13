#!/bin/bash

export FLASK_APP=manticora
export FLASK_DEBUG=1

python migrations.py db init
python migrations.py db migrate
python migrations.py db upgrade
python manage.py runserver
