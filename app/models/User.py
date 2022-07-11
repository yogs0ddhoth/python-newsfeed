from app.db import Base
from sqlalchemy import Column, Integer, String, true

class User(Base):
  __tablename__ = 'users'
  id = Column(Integer, primary_key = True)
  username = Column(String(50), nullable = False)
  email = Column(String(50), nullable = False, unique = True)
  password = Column(String(100), nullable = False)
