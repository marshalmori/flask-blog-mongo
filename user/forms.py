from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms.validators import ValidationError
import re

from user.models import User

class RegisterForm(FlaskForm):
    first_name = StringField('Primeiro Nome', [validators.DataRequired()])
    last_name = StringField('Último Nome', [validators.DataRequired()])
    email = EmailField('Email', [
            validators.DataRequired(),
            validators.Email()
            ]
        )
    username = StringField('Nome de Usuário', [
            validators.DataRequired(),
            validators.length(min=4, max=25)
            ]
        )
    password = PasswordField('Senha', [
            validators.DataRequired(),
            validators.EqualTo('confirm', message='As senhas devem ser iguais.'),
            validators.length(min=4, max=80)
            ]
        )
    confirm = PasswordField('Confirmar Senha:')

    def validate_username(form, field):
        if User.objects.filter(username=field.data).first():
            raise ValidationError('Nome de usuário já cadastrado.')
        if not re.match("^[a-zA-Z0-9_-]{4,25}$", field.data):
            raise ValidationError('Nome de usuário inválido. Use somente letras, números e underline e traço')

    def validate_email(form, field):
        if User.objects.filter(email=field.data).first():
            raise ValidationError('Email já cadastrado.')

class LoginForm(FlaskForm):
    username = StringField('Nome de Usuário', [
            validators.DataRequired(),
            validators.length(min=4, max=25)
            ]
        )
    password = PasswordField('Senha', [
            validators.DataRequired(),
            validators.length(min=4, max=80)
            ]
        )
