import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import SingletonThreadPool

def create_session():
    engine = create_engine('sqlite:///restaurantmenu.db', poolclass=SingletonThreadPool)
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session