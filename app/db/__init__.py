from os import getenv
from flask import g
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv() # load db url from .env

# connect to db with .env variable
engine = create_engine(getenv('DB_URL'), echo = True, pool_size = 20, max_overflow = 0)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def init_db():
  Base.metadata.create_all(engine)

def get_db():
  if 'db' not in g: # if db connection does not exist
    g.db = Session() # connect to database and store in app context
  
  return g.db # return connection