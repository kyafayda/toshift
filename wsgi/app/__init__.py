import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir, ADMINS, MAIL_SERVER, MAIL_PORT
from config import MAIL_USERNAME, MAIL_PASSWORD
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

lm = LoginManager()
lm.setup_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

#if not app.debug:
#import logging
 #   from logging.handlers import SMTPHandler
  #  credentials = None
  #  if MAIL_USERNAME or MAIL_PASSWORD:
  #      credentials = (MAIL_USERNAME, MAIL_PASSWORD)
  #  mail_handler = SMTPHandler((MAIL_SERVER, MAIL_PORT), 'no-reply@'
  #          + MAIL_SERVER, ADMINS, 'expense_app failure', credentials)
  #  mail_handler.setlevel(logging.ERROR)
  #  app.logger.addHandler(mail_handler)
from app import routes, models
