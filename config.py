import os
basedir = os.path.abspath(os.path.dirname(__file__)) # main directory of application

class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	# location of the application's database
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or 'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = False	
	LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')