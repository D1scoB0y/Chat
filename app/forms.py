from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField
    )


class RegistrationForm(FlaskForm):

    username = StringField('username', validators=[DataRequired(), Length(min=3, max=25)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=255)])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('submit')


class LoginForm(FlaskForm):

    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=255)])
    remember_me = BooleanField('remember_me')

    submit = SubmitField('submit')
    