from flask_wtf import FlaskForm
from wtforms import validators, StringField, PasswordField
from wtforms.fields.html5 import EmailField

class RegisterForm(FlaskForm):
    first_name = StringField('Primeiro Nome:', [validators.Required()])
    last_name = StringField('Último Nome:', [validators.Required()])
    email = EmailField('Email:', [
            validators.DataRequired(),
            validators.Email()
            ]
        )
    username = StringField('Nome de Usuário:', [
            validators.Required(),
            validators.length(min=4, max=25)
            ]
        )
    password = PasswordField('Senha:', [
            validators.Required(),
            validators.EqualTo('confirm', message='As senhas devem ser iguais.'),
            validators.length(min=4, max=80)
            ]
        )
    confirm = PasswordField('Confirmar Senha:')
