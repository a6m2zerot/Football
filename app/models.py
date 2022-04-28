from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String())

    def set_password(self, password):  # TODO откуда берется password?
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class GameStats(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    meteor_goal = db.Column(db.Integer())  # amount of goals by Meteor
    rocket_goal = db.Column(db.Integer())
    meteor_score = db.Column(db.Integer())  # if winner -> gives 3 pts, if loser -> gives 0 pts, if draw -> 1 pt.
    rocket_score = db.Column(db.Integer())


@login.user_loader
def load_user(id):
    return User.query.get(int(id))

