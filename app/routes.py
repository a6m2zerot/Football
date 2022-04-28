from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.models import User, GameStats
from flask_login import current_user, login_user, logout_user


@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        a = request.form["floatingInput"]
        b = request.form["floatingPassword"]
        user = User.query.filter_by(username=a).first()

        if user is None or not user.check_password(b):
            flash('Invalid username or password')
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for('index'))

    return render_template("login.html")


@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        meteor_goal = request.form["meteor_goal"]
        rocket_goal = request.form["rocket_goal"]

        if meteor_goal > rocket_goal:
            m = GameStats(meteor_goal=meteor_goal, rocket_goal=rocket_goal, meteor_score=3, rocket_score=0)
            db.session.add(m)
            db.session.commit()
            request.close()
            return redirect("/index", 302)
        elif meteor_goal == rocket_goal:
            w = GameStats(meteor_goal=meteor_goal, rocket_goal=rocket_goal, meteor_score=1, rocket_score=1)
            db.session.add(w)
            db.session.commit()
            request.close()
            return redirect("/index", 302)
        else:
            r = GameStats(meteor_goal=meteor_goal, rocket_goal=rocket_goal, meteor_score=0, rocket_score=3)
            db.session.add(r)
            db.session.commit()
            request.close()
            return redirect("/index", 302)

    array_of_games = GameStats.query.all()

    sss = GameStats.query.all()
    meteor_score_total, meteor_goal_total = 0, 0
    rocket_score_total, rocket_goal_total = 0, 0
    for elem in sss:
        meteor_score_total = meteor_score_total + elem.meteor_score  # Набранные очки Метеором
        rocket_score_total = rocket_score_total + elem.rocket_score  # Набранные очки Ракетой
        meteor_goal_total = meteor_goal_total + elem.meteor_goal  # Забитые голы Метеором
        rocket_goal_total = rocket_goal_total + elem.rocket_goal  # Забитые голы Ракетой

    return render_template("index.html", array_of_games=array_of_games,
                                         meteor_score_total=meteor_score_total,
                                         rocket_score_total=rocket_score_total,
                                         meteor_goal_total=meteor_goal_total,
                                         rocket_goal_total=rocket_goal_total)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

