from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email: ', validators=[Email()])
    password = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=5, max=50)])
    remember = BooleanField('Запомнить', default=False)
    submit = SubmitField('Войти')

class RegistrForm(FlaskForm):
    username = StringField('Логин: ', validators=[Length(min= 5, max= 40, message='Имя должно быть от 5 до 40 символов')])
    email = StringField('Email: ', validators=[Email('Некорректный email')])
    password = PasswordField('Пароль: ', validators=[DataRequired(), Length(min=5, max=50, message='Пароль должен быть от 5 до 50 символов')])
    repeate_password = PasswordField('Повторите пароль: ', validators=[DataRequired(),
                                                                       EqualTo('password',  message='Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')