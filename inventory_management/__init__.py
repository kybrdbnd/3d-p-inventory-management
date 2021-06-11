import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

basedir = os.getcwd()
app = Flask(__name__)
Bootstrap(app)

app.config.update({
    'SQLALCHEMY_DATABASE_URI': 'postgresql://postgres:postgres@localhost/inventory_management',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SECRET_KEY': '234234243234243234234'
})

# sqlalchemy instance
db = SQLAlchemy(app)
ma = Marshmallow(app)

migrate = Migrate(app, db)

from .inventory import inventory

app.register_blueprint(inventory)
