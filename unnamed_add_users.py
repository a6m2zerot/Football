from app.models import User, Teams1, Teams2, TeamStats, Players
from app import db

a = User(username="Андрей")
a.set_password("111")
db.session.add(a)

d = User(username="Богдан")
d.set_password("222")
db.session.add(d)

teamname = ["Rocket", "Comet", "Meteor"]
for elem in teamname:
    db.session.add(Teams1(teamname=elem))
    db.session.add(Teams2(teamname=elem))

for i in teamname:
    f = TeamStats(teamname=i, team_id_overall_games=0,
            team_id_overall_goals=0,
            team_id_overall_passed_goals=0,
            team_id_overall_score=0)
    db.session.add(f)

rocket_players = ["Rybakov", "Rogov", "Rashkin"]
for elem_1 in rocket_players:
    r = Players(player=elem_1, player_team="Rocket", player_goals=0)
    db.session.add(r)

comet_players = ["Corovin", "Crasavin", "Cravtchuk"]
for elem_2 in comet_players:
    c = Players(player=elem_2, player_team="Comet", player_goals=0)
    db.session.add(c)

meteor_players = ["Markin", "Milov", "Matveev"]
for elem_3 in meteor_players:
    m = Players(player=elem_3, player_team="Meteor", player_goals=0)
    db.session.add(m)

db.session.commit()
