from flask import session, redirect
from functools import wraps

def login_required(func):
  @wraps(func)
  def wrapped_function(*args, **kwargs):
    if session.get('loggedIn') == True: # if logged in, call func()
      return func(*args, **kwargs)
    return redirect('/login') # else redirect to '/login'

  return wrapped_function
