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
    print('validation error')
    db.rollback()
    return jsonify(message = 'Signup failed'), 500

  except sqlalchemy.exc.IntegrityError:
    print('mysql error')
    db.rollback()
    return jsonify(message = 'Signup failed'), 500

  session.clear()
  session['user_id'] = newUser.id
  session['loggedIn'] = True
  return jsonify(id = newUser.id)