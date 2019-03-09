from __future__ import absolute_import

from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from . import main
from .form import StudentLoginForm, StudentSignUpForm


@main.route("/")
def index():
    return render_template("base.html")


@main.route("/login", methods=("GET",))
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for(".home_page"))

    form = StudentLoginForm()
    return render_template("login.html", form=form)


@main.route("/signup", methods=("GET",))
def signup_page():
    form = StudentSignUpForm()
    return render_template("signup.html", form=form)


@main.route("/account/home")
@login_required
def home_page():
    return "Hello, " + current_user.name
