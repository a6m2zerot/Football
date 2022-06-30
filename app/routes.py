from app import app, db
from flask import render_template, request, redirect, url_for, flash
from app.models import User, GameStats, Teams1, Teams2, TeamStats, Players, Players_Goals
from flask_login import current_user, login_user, logout_user, login_required
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
@login_required
def index():
    if request.method == "POST":
        first = int(request.form["1st_team_goal"])
        first_player_id = int(request.form["1st_player_id"])
        second = int(request.form["2nd_team_goal"])
        second_player_id = int(request.form["2nd_player_id"])

        first_team_name = Players.query.filter_by(id=first_player_id).first().player_team  # получаем название команды по игроку
        first_id = Teams1.query.filter_by(teamname=first_team_name).first().id  # получаем id команды по ее названию
        player_1_name = Players.query.get(first_player_id).player
        player_2_name = Players.query.get(second_player_id).player

        second_team_name = Players.query.filter_by(id=second_player_id).first().player_team
        second_id = Teams2.query.filter_by(teamname=second_team_name).first().id

        if first != "" and second != "" and first_id != "0" and second_id != "0" and first_id != second_id:
            if first == 0 and second != 0:
                first_teamname = Teams1.query.get(first_id).teamname
                second_teamname = Teams1.query.get(second_id).teamname

                z_2 = Players.query.filter_by(player=player_2_name).first()
                z_2.player_goals = z_2.player_goals + second

                qw = GameStats.query.all()
                total = len(qw) + 1
                sss_2 = Players_Goals(game_number=total, player_id=second_player_id, number_of_goals=second)
                db.session.add_all([z_2, sss_2])
                db.session.commit()
            elif second == 0 and first != 0:
                first_teamname = Teams1.query.get(first_id).teamname
                second_teamname = Teams1.query.get(second_id).teamname

                z_1 = Players.query.filter_by(
                    player=player_1_name).first()  # вводим инфу в Players для сбора статистики
                z_1.player_goals = z_1.player_goals + first

                qw = GameStats.query.all()
                total = len(qw) + 1
                sss_1 = Players_Goals(game_number=total, player_id=first_player_id, number_of_goals=first)
                db.session.add_all([z_1, sss_1])
                db.session.commit()
            elif first == 0 and second == 0:
                first_teamname = Teams1.query.get(first_id).teamname
                second_teamname = Teams1.query.get(second_id).teamname
            else:
                first_teamname = Teams1.query.get(first_id).teamname
                second_teamname = Teams1.query.get(second_id).teamname

                z_1 = Players.query.filter_by(player=player_1_name).first()  # вводим инфу в Players для сбора статистики
                z_2 = Players.query.filter_by(player=player_2_name).first()
                z_1.player_goals = z_1.player_goals + first
                z_2.player_goals = z_2.player_goals + second

                qw = GameStats.query.all()
                total = len(qw) + 1
                sss_1 = Players_Goals(game_number=total, player_id=first_player_id, number_of_goals=first)
                sss_2 = Players_Goals(game_number=total, player_id=second_player_id, number_of_goals=second)
                db.session.add_all([z_1, z_2, sss_1, sss_2])
                db.session.commit()

            if first > second:
                m = GameStats(goals_1=first, goals_2=second, passed_goals_1=second, passed_goals_2=first, score_1=3,
                              score_2=0, teamname_id_1=first_id, teamname_id_2=second_id)
                k_1 = TeamStats.query.filter_by(teamname=first_teamname).first()  # .first получает объект, а .all получает массив объекта
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
    array_of_users = User.query.all()
    array_of_players = Players.query.all()
    return render_template("index.html", array_of_teams_1=array_of_teams_1, array_of_teams_2=array_of_teams_2,
                           array_of_games=array_of_games, array_of_games_per_team=array_of_games_per_team,
                           array_of_users=array_of_users, array_of_players=array_of_players)


@app.route("/new_game", methods=["GET", "POST"])  # создаем новую игру при нажатии на +Add
@login_required
def create_new_game():
    if request.method == "POST":
        first_team_id = int(request.form["first_team_id"])
        second_team_id = int(request.form["second_team_id"])

        if first_team_id and second_team_id:
            a = Teams1.query.filter_by(id=first_team_id).first().teamname
            b = Teams1.query.filter_by(id=second_team_id).first().teamname
            players_b = Players.query.filter_by(player_team=b).all()
            players_a = Players.query.filter_by(player_team=a).all()
            array_of_teams_1 = Teams1.query.all()
            array_of_teams_2 = Teams2.query.all()
            array_of_players = Players.query.all()
            return render_template("new_game.html", array_of_teams_1=array_of_teams_1,
                                   array_of_teams_2=array_of_teams_2,
                                   array_of_players=array_of_players, players_a=players_a, players_b=players_b, a=a,
                                   b=b)

    array_of_teams_1 = Teams1.query.all()
    array_of_teams_2 = Teams2.query.all()
    array_of_players = Players.query.all()
    return render_template("new_game.html", array_of_teams_1=array_of_teams_1, array_of_teams_2=array_of_teams_2,
                           array_of_players=array_of_players)


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

    f = Players.query.all()
    for j in range(len(f)):
        f[j].player_goals = 0
        db.session.add(f[j])
    db.session.commit()
    return redirect("/index", 302)


@app.route("/delete_game_stats/<int:game_number>")
def delete_game_stats(game_number):  # удаление статистики одной конретной игры
    # update TeamStats for players
    a = GameStats.query.get(game_number)
    if a.goals_1 == 0 and a.goals_2 == 0:
        pass
    elif a.goals_1 != 0 and a.goals_2 == 0:
        pl_1 = Players.query.filter_by(player=a.playerstats[0].players.player).first()
        pl_1.player_goals = pl_1.player_goals - a.goals_1
        db.session.add(pl_1)
    elif a.goals_1 == 0 and a.goals_2 != 0:
        pl_2 = Players.query.filter_by(player=a.playerstats[0].players.player).first()
        pl_2.player_goals = pl_2.player_goals - a.goals_2
        db.session.add(pl_2)
    else:
        pl_1 = Players.query.filter_by(player=a.playerstats[0].players.player).first()
        pl_1.player_goals = pl_1.player_goals - a.goals_1
        pl_2 = Players.query.filter_by(player=a.playerstats[1].players.player).first()
        pl_2.player_goals = pl_2.player_goals - a.goals_2
        db.session.add_all([pl_1, pl_2])

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
    return redirect("/index", 302)


@app.route("/stats/<teamname>")
@login_required
def get_stats(teamname):
    obj = TeamStats.query.filter_by(teamname=teamname).first()
    return render_template("stats.html", obj=obj)


@app.route("/test")  # тестовый рут
def test():
    return render_template("test.html")
