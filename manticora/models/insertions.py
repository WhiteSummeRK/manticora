from tables import User, db

db.create_all()

Kauan = User(name='Kauan Alves', pwd='K123', bill=123.50)

db.session.add(Kauan)
db.session.commit()

User.query.all()
