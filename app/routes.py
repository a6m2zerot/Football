from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.models import User, GameStats, Teams1, Teams2, TeamStats, Players
from flask_login import current_user, login_user, logout_user
from app.forms import RegistrationForm


@app.route("/registration_form", methods=["POST", "GET"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    reg = RegistrationForm()
    if reg.validate_on_submit():
        user = User(username=reg.username.data)
        user.set_password(reg.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user! Please log in.')
        return redirect(url_for('login'))
    return render_template("registration_form.html", form=reg)


@app.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        a = request.form["floatingInput"]
        b = request.form["floatingPassword"]
        user = User.query.filter_by(username=a).first()

        if user is None or not user.check_password(b):
            flash('Invalid username or password. Please try again.')
            return redirect(url_for("login"))
        login_user(user)
        return redirect(url_for('index'))

    return render_template("login.html")


@app.route("/index", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        first = int(request.form["1st_team_goal"])
        first_id = request.form["first_id"]
        second = int(request.form["2nd_team_goal"])
        second_id = request.form["second_id"]

        if first != "" and second != "" and first_id != "0" and second_id != "0" and first_id != second_id:  # проверка на корректное заполнение полей
            first_teamname = Teams1.query.get(first_id).teamname
            second_teamname = Teams1.query.get(second_id).teamname
            if first > second:
                m = GameStats(goals_1=first, goals_2=second, passed_goals_1=second, passed_goals_2=first, score_1=3,
                              score_2=0, teamname_id_1=first_id, teamname_id_2=second_id)
                k_1 = TeamStats.query.filter_by(
                    teamname=first_teamname).first()  # .first получает объект, а .all получает массив объекта
                k_1.team_id_overall_games = k_1.team_id_overall_games + 1
                k_1.team_id_overall_goals = k_1.team_id_overall_goals + first
                k_1.team_id_overall_passed_goals = k_1.team_id_overall_passed_goals + second
                k_1.team_id_overall_score = k_1.team_id_overall_score + 3

                k_2 = TeamStats.query.filter_by(teamname=second_teamname).first()
                k_2.team_id_overall_games = k_2.team_id_overall_games + 1
                k_2.team_id_overall_goals = k_2.team_id_overall_goals + second
                k_2.team_id_overall_passed_goals = k_2.team_id_overall_passed_goals + first
                k_2.team_id_overall_score = k_2.team_id_overall_score + 0

                db.session.add_all([m, k_1, k_2])
                db.session.commit()
                request.close()
                return redirect("/index", 302)
            elif first == second:
                w = GameStats(goals_1=first, goals_2=second, passed_goals_1=second, passed_goals_2=first, score_1=1,
                              score_2=1, teamname_id_1=first_id, teamname_id_2=second_id)

                k_1 = TeamStats.query.filter_by(teamname=first_teamname).first()
                k_1.team_id_overall_games = k_1.team_id_overall_games + 1
                k_1.team_id_overall_goals = k_1.team_id_overall_goals + first
                k_1.team_id_overall_passed_goals = k_1.team_id_overall_passed_goals + second
                k_1.team_id_overall_score = k_1.team_id_overall_score + 1

                k_2 = TeamStats.query.filter_by(teamname=second_teamname).first()
                k_2.team_id_overall_games = k_2.team_id_overall_games + 1
                k_2.team_id_overall_goals = k_2.team_id_overall_goals + second
                k_2.team_id_overall_passed_goals = k_2.team_id_overall_passed_goals + first
                k_2.team_id_overall_score = k_2.team_id_overall_score + 1

                db.session.add_all([w, k_1, k_2])
                db.session.commit()
                request.close()
                return redirect("/index", 302)
            else:
                r = GameStats(goals_1=first, goals_2=second, passed_goals_2=first, passed_goals_1=second, score_1=0,
                              score_2=3, teamname_id_1=first_id, teamname_id_2=second_id)
                k_1 = TeamStats.query.filter_by(teamname=first_teamname).first()
                k_1.team_id_overall_games = k_1.team_id_overall_games + 1
                k_1.team_id_overall_goals = k_1.team_id_overall_goals + first
                k_1.team_id_overall_passed_goals = k_1.team_id_overall_passed_goals + second
                k_1.team_id_overall_score = k_1.team_id_overall_score + 0

                k_2 = TeamStats.query.filter_by(teamname=second_teamname).first()
                k_2.team_id_overall_games = k_2.team_id_overall_games + 1
                k_2.team_id_overall_goals = k_2.team_id_overall_goals + second
                k_2.team_id_overall_passed_goals = k_2.team_id_overall_passed_goals + first
                k_2.team_id_overall_score = k_2.team_id_overall_score + 3

                db.session.add_all([r, k_1, k_2])
                db.session.commit()
                request.close()
                return redirect("/index", 302)
        else:
            flash("Incorrect Input. Please, try again!")
            return redirect("/index")

    array_of_teams_1 = Teams1.query.all()
    array_of_teams_2 = Teams2.query.all()
    array_of_games = GameStats.query.all()  # количество игр всего
    array_of_games_per_team = TeamStats.query.all()  # количество игр по конкретной команде (по ID)
    return render_template("index.html", array_of_teams_1=array_of_teams_1, array_of_teams_2=array_of_teams_2,
                           array_of_games=array_of_games, array_of_games_per_team=array_of_games_per_team)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/delete_all_stats")
def delete_all_stats():  # удаление статистики всех игр
    db.session.query(GameStats).delete()
    obj = TeamStats.query.all()
    for i in range(len(obj)):
        obj[i].team_id_overall_games = 0
        obj[i].team_id_overall_goals = 0
        obj[i].team_id_overall_passed_goals = 0
        obj[i].team_id_overall_score = 0
        db.session.add(obj[i])
    db.session.commit()
    return redirect("/index", 302)


@app.route("/delete_game_stats/<int:game_number>")
def delete_game_stats(game_number):  # удаление статистики одной конретной игры
    a = GameStats.query.get(game_number)
    obj_1 = TeamStats.query.filter_by(teamname=a.teams1.teamname).first()
    obj_2 = TeamStats.query.filter_by(teamname=a.teams2.teamname).first()
    # update TeamStats for obj_1   :
    obj_1.team_id_overall_games = obj_1.team_id_overall_games - 1
    obj_1.team_id_overall_goals = obj_1.team_id_overall_goals - a.goals_1
    obj_1.team_id_overall_passed_goals = obj_1.team_id_overall_passed_goals - a.passed_goals_1
    obj_1.team_id_overall_score = obj_1.team_id_overall_score - a.score_1

    # update TeamStats for obj_2   :
    obj_2.team_id_overall_games = obj_2.team_id_overall_games - 1
    obj_2.team_id_overall_goals = obj_2.team_id_overall_goals - a.goals_2
    obj_2.team_id_overall_passed_goals = obj_2.team_id_overall_passed_goals - a.passed_goals_2
    obj_2.team_id_overall_score = obj_2.team_id_overall_score - a.score_2

    db.session.add_all([obj_1, obj_2])
    db.session.query(GameStats).filter(GameStats.id == game_number).delete()
    db.session.commit()
    """
    2-ой вариант 
    attr = Gamestats.query.get(game_number)
    db.session.delete(attr)
    db.session.commit()
    """
    return redirect("/index", 302)


"""
UPDATE \ Обновление
1.Получение объекта 
2. Изменение конкретного поля объекта
3. Добавление в сессию измененного объекта
4. Сохранение изменений

attr = GameStats.query.get(1)
attr.meteor_goals = 10
attr.rocket_goals = 2
db.session.add(attr)
db.session.commit()
"""


@app.route("/stats/<teamname>")
def get_stats(teamname):
    obj = TeamStats.query.filter_by(teamname=teamname).first()
    return render_template("stats.html", obj=obj)


@app.route("/test")  # тестовый рут
def test():
    return render_template("test.html")
