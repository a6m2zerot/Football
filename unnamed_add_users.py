from app.models import User
from app import db

a = User(username="Андрей")
a.set_password("111")
db.session.add(a)

d = User(username="Богдан")
d.set_password("222")
db.session.add(d)

g = User(username="Виктор")
g.set_password("333")
db.session.add(g)

db.session.commit()
