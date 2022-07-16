from email import message
import sys
from flask import Blueprint, request, jsonify, session
import sqlalchemy
from app.models import User
from app.db import get_db

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
  data = request.get_json() # create new data dict from request
  db = get_db() # connect to database
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