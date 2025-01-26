from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import re

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    exercises = db.relationship('ExerciseResult', backref='user', lazy='dynamic')

    def set_password(self, password):
        if not re.match(
            r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
            password
        ):
            raise ValueError(
                'Hasło musi zawierać: 1 dużą literę, 1 małą literę, 1 cyfrę i 1 znak specjalny (@$!%*?&)'
            )
        self.password_hash = generate_password_hash(password, method='pbkdf2:sha256')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Verb(db.Model):
    __tablename__ = 'verbs'
    id = db.Column(db.Integer, primary_key=True)
    base_form = db.Column(db.String(64), nullable=False)
    masu_form = db.Column(db.String(64), nullable=False)
    eng = db.Column(db.String(256))
    pl = db.Column(db.String(256))

class Kanji(db.Model):
    __tablename__ = 'kanji'
    id = db.Column(db.Integer, primary_key=True)
    character = db.Column(db.String(1), nullable=False)
    on_yomi = db.Column(db.String(256))
    kun_yomi = db.Column(db.String(256))
    meanings = db.Column(db.String(256))

class ExerciseResult(db.Model):
    __tablename__ = 'exercise_results'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    exercise_type = db.Column(db.String(64))
    score = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index=True, default=db.func.now())