from flask import Blueprint, render_template, request, redirect, session, url_for, abort
import bcrypt

from user.models import User
from user.forms import RegisterForm

user_app = Blueprint('user_app', __name__)

@user_app.route('/login')
def login():
    return 'User login'


@user_app.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print('Entrou')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data.encode('utf-8'), salt)
        user = User(
            username=form.username.data,
            password=hashed_password,
            email=form.email.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            )
        user.save()
        print('Salvou no bando de dados')
        return 'Deu certo'
    return render_template('user/register.html', form=form)
