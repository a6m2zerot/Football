from app.models import User, Teams1, Teams2, TeamStats
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


db.session.commit()
