#! /usr/bin/env python

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm
from .forms import LoginForm, RegisterForm
from .models import User

@lm.user_loader
def load_user(userid):
    return db.session.query(User).get(userid)

@app.before_request
def before_request():
    g.user = current_user

@app.route("/")
@app.route("/index")
@login_required
def index():
    user = g.user
    posts = [
        {
            'author':{'nickname':'john'},
            'body':'shit'
        },
        {
            'author':{'nickname':'susan'},
            'body':'damn'
        }
        ]
    return render_template('base.html',
        title = 'home',
        user = user,
        posts = posts)

@app.route("/login", methods = ["get", "post"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        session["userid"] = form.user.id
        #login_user(session["user_id"])
        return redirect(url_for("index"))
    return render_template("login.html",
                           title = "sign in",
                           form = form,
                           )

@app.route("/register", methods = ["get", "post"])
def register():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        user = User(username = form.username.data,
                    password = form.password.data,
                    email    = form.email.data)
        db.session.add(user)
        db.session.commit()
        session["remember_me"] = form.remember_me.data
        return redirect(request.args.get("next") or url_for("index"))
    return render_template("register.html",
                           title = "sign in",
                           form = form,
                           )

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
