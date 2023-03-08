import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://root:mudar123@postgres_db:5432/demo'



class Development(Config):
    DEVELOPMENT = True
    DEBUG = True
