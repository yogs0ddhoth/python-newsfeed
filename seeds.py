from app.models import User
from app.db import Session, Base, engine

# drop and rebuild tables
Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)

db = Session()

# insert users
db.add_all(
  [
    User(username='seed1', email='seed1@cbc.ca', password='password123'),
    User(username='seed2', email='seed2@sogou.com', password='password123'),
    User(username='seed3', email='seed3@last.fm', password='password123'),
    User(username='seed4', email='seed4@goo.ne.jp', password='password123'),
    User(username='seed5', email='seed5@weather.com', password='password123')
  ]
)
db.commit()
db.close()