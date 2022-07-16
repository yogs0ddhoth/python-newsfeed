from flask import Blueprint, render_template, session, redirect

from app.models import Post
from app.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')

@bp.route('/')
def index():
  db = get_db() # connect to the database
  posts = (
    db # get all posts, order by datetime created_at
      .query(Post)
      .order_by(Post.created_at.desc())
      .all()
  )
  return render_template( # pass session[loggedIn] to templates
    'homepage.html', posts=posts, loggedIn=session.get('loggedIn')
  )

@bp.route('/login')
def login():
  return render_template('login.html')

@bp.route('/post/<id>')
def single(id):
  db = get_db() # connect to the database
  post = (
    db # get single post by id
      .query(Post)
      .filter(Post.id == id)
      .one()
  )
  return render_template( # pass session[loggedIn] to templates
    'single-post.html', post=post, loggedIn=session.get('loggedIn')
  )