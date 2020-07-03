import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://test:mudar123@test.cz5xowyke5ys.sa-east-1.rds.amazonaws.com/postgres'



class Development(Config):
    DEVELOPMENT = True
    DEBUG = True
