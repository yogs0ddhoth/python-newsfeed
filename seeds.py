from app.models import User, Post
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
#  insert posts
db.add_all(
  [
    Post(
      title='Donec posuere metus vitae ipsum', 
      post_url='https://buzzfeed.com/in/imperdiet/et/commodo/vulputate.png', 
      user_id=1
    ),
    Post(
      title='Morbi non quam nec dui luctus rutrum', 
      post_url='https://nasa.gov/donec.json', 
      user_id=1
    ),
    Post(
      title='Donec diam neque, vestibulum eget, vulputate ut, ultrices vel, augue', 
      post_url='https://europa.eu/parturient/montes/nascetur/ridiculus/mus/etiam/vel.aspx', 
      user_id=2
    ),
    Post(
      title='Nunc purus', 
      post_url='http://desdev.cn/enim/blandit/mi.jpg', 
      user_id=3
    ),
    Post(
      title='Pellentesque eget nunc', 
      post_url='http://google.ca/nam/nulla/integer.aspx', 
      user_id=4
    )
  ]
)
db.commit()
db.close()