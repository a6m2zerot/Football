from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
app.config["SECRET_KEY"] = "you-will-never-guess"
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL") or \
                                "sqlite:///" + os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)

login = LoginManager(app)

from app import models, routes



