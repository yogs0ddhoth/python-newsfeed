from flask import Blueprint, render_template, session, redirect

from app.models import Post
from app.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def index():
  db = get_db() # connect to the database
  posts = ( # get all posts, order by datetime created_at
    db.query(Post)
      .order_by(Post.created_at.desc())
      .all()
  )
  return render_template( # pass session[loggedIn] to templates
    'homepage.html', posts=posts, loggedIn=session.get('loggedIn')
  )

@bp.route('/login')
def login():
  if session.get('loggedIn') is None:
    return render_template('login.html')
  return redirect('/dashboard')

@bp.route('/post/<id>')
def single(id):
  db = get_db() # connect to the database
  post = ( # get single post by id
    db.query(Post)
      .filter(Post.id == id)
      .one()
  )
  return render_template( # pass session[loggedIn] to templates
    'single-post.html', post=post, loggedIn=session.get('loggedIn')
  )