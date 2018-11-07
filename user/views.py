from flask import Blueprint, render_template, request, redirect, session, url_for, abort
from user.forms import RegisterForm

user_app = Blueprint('user_app', __name__)

@user_app.route('/login')
def login():
    return 'User login'


@user_app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    return render_template('user/register.html', form=form)
