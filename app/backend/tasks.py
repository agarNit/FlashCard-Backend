import datetime as dt, os
from flask_mail import Message, Mail
from backend.db import Db
from flask import current_app as app

mail = Mail(app)

