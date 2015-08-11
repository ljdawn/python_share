#! /usr/bin/env python

import os
from flask import Flask
from flask.ext.login import LoginManager
from config import basedir
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
lm = LoginManager()
lm.init_app(app)
lm.login_view = "login"
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
