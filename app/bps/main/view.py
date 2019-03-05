from __future__ import absolute_import

from flask import render_template

from . import main
from .form import StudentLoginForm


@main.route("/")
def index():
    return render_template("base.html")


@main.route("/login", methods=("GET",))
def login_page():
    form = StudentLoginForm()
    return render_template("login.html", form=form)
