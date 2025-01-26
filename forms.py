from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import DataRequired, EqualTo, Length, Regexp

class RegistrationForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[
        DataRequired(message='Nazwa użytkownika jest wymagana')
    ])
    password = PasswordField('Hasło', validators=[
        DataRequired(message='Hasło jest wymagane'),
        Length(min=8, message='Hasło musi mieć minimum 8 znaków'),
        Regexp(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            message='Hasło musi zawierać: 1 dużą literę, 1 małą literę, 1 cyfrę i 1 znak specjalny (@$!%*?&)'
        )
    ])
    password2 = PasswordField('Powtórz hasło', validators=[
        DataRequired(message='Proszę powtórzyć hasło'),
        EqualTo('password', message='Hasła muszą być identyczne')
    ])
    submit = SubmitField('Zarejestruj się')

class LoginForm(FlaskForm):
    username = StringField('Nazwa użytkownika', validators=[DataRequired()])
    password = PasswordField('Hasło', validators=[DataRequired()])
    submit = SubmitField('Zaloguj się')

class VerbExerciseForm(FlaskForm):
    verb = HiddenField('Czasownik')
    user_input = StringField('Twoja odpowiedź', validators=[DataRequired()])
    submit = SubmitField('Sprawdź')

class KanjiExerciseForm(FlaskForm):
    kanji = HiddenField('Kanji')
    user_input = StringField('Twoja odpowiedź', validators=[DataRequired()])
    submit = SubmitField('Sprawdź')