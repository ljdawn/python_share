#! /usr/bin/env python

from flask import Flask
from flask_admin import Admin, BaseView, expose

class MyView(BaseView):
    @expose("/")
    def index(self):
        return self.render("index.html")

app = Flask(__name__)

admin = Admin(app, name="Asa")
admin.add_view(MyView(name="hello"))

app.run(debug = True)
