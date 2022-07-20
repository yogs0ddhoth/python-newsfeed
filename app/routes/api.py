import sys
from flask import Blueprint, request, jsonify, session
import sqlalchemy
from app.models import User, Post, Comment, Vote
from app.db import get_db
from app.utils.auth import login_required

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])
def signup():
  data = request.get_json() # create new data dict from request
  db = get_db() # connect to database
  try:
    newUser = User( # create new User
      username = data['username'],
      email = data['email'],
      password = data['password']
    )
    db.add(newUser)
    db.commit() # save User to database
    print('Success!')
  except AssertionError: # log errors
    print('Validation error')
    db.rollback()
    return jsonify(message = 'Signup failed'), 500
  except sqlalchemy.exc.IntegrityError:
    print('MySQL error')
    db.rollback()
    return jsonify(message = 'Signup failed'), 500

  session.clear() # clear sesion, add: {user_id: newUser.id, loggedIn: True}
  session['user_id'] = newUser.id
  session['loggedIn'] = True
  return jsonify(id = newUser.id)

@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()
  try:
    user = ( # get single user by email
      db.query(User)
        .filter(User.email == data['email'])
        .one()
    )
  except sqlalchemy.exc.NoResultFound:
    print('No result found')
    return jsonify(message = 'Incorrect credentials'), 400
  
  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400
  
  session.clear()
  session['user_id'] = user.id
  session['loggedIn'] = True
  return jsonify(id = user.id)

@bp.route('/users/logout', methods=['POST'])
def logout(): # remove session variables
  session.clear()
  return '', 204

@bp.route('/posts', methods=['POST'])
@login_required
def create():
  data = request.get_json()
  db = get_db()
  try:
    newPost = Post( # create new Post
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )
    db.add(newPost)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post failed'), 500

  return jsonify(id = newPost.id)

@bp.route('/posts/<id>', methods=['PUT'])
@login_required # require the user to be logged in
def update(id):
  data = request.get_json()
  db = get_db()
  try:
    post = ( # query Posts, retrieve single Post by id
      db.query(Post)
        .filter(Post.id == id)
        .one()
    )
    post.title = data['title'] # update title
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404
  
  return '', 204

@bp.route('/posts/<id>', methods=['DELETE'])
@login_required
def delete(id):
  db = get_db()
  try:
    db.delete( # delete:
      db.query(Post) # single Post by id
        .filter(Post.id == id)
        .one()
    )
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404
  
  return '', 204

@bp.route('/posts/upvote', methods=['PUT'])
@login_required
def upvote():
  data = request.get_json()
  db = get_db()
  try:
    newVote = Vote( # create new Vote 
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )
    db.add(newVote)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Upvote failed'), 500
  
  return '', 204

@bp.route('/comments', methods=['Post'])
@login_required
def comment():
  data = request.get_json()
  db = get_db()
  try:
    newComment = Comment( # create new Comment
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )
    db.add(newComment)
    db.commit()
  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Comment failed'), 500

  return jsonify(id = newComment.id)