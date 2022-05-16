from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30))
    password_hash = db.Column(db.String())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class GameStats(db.Model):  # статистика отдельной игры
    id = db.Column(db.Integer(), primary_key=True)
    goals_1 = db.Column(db.Integer())  # забитые мячи
    passed_goals_1 = db.Column(db.Integer())  # пропущенные мячи
    score_1 = db.Column(db.Integer())  # if winner -> gives 3 pts, if loser -> gives 0 pts, if draw -> 1 pt
    teamname_id_1 = db.Column(db.Integer(), db.ForeignKey("teams1.id"))

    goals_2 = db.Column(db.Integer())
    passed_goals_2 = db.Column(db.Integer())
    score_2 = db.Column(db.Integer())
    teamname_id_2 = db.Column(db.Integer(), db.ForeignKey("teams2.id"))


class Teams1(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    teamname = db.Column(db.String(20))
    gamestats = db.relationship("GameStats", backref="teams1")


class Teams2(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    teamname = db.Column(db.String(20))
    gamestats = db.relationship("GameStats", backref="teams2")


class TeamStats(db.Model):  # статистика отдельной команды
    id = db.Column(db.Integer(), primary_key=True)
    teamname = db.Column(db.String())
    team_id_overall_games = db.Column(db.Integer())
    team_id_overall_goals = db.Column(db.Integer())
    team_id_overall_passed_goals = db.Column(db.Integer())
    team_id_overall_score = db.Column(db.Integer())


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
