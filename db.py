from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from config import Development

Session = sessionmaker(autocommit=False, autoflush=False, bind=create_engine(Development.SQLALCHEMY_DATABASE_URI))
session = scoped_session(Session)