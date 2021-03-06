from flask import Flask, make_response, render_template
from backend.database import db
from backend import workers
from backend.config import LocalDevelopmentConfig
from flask_cors import CORS
from flask_mail import Message, Mail
from backend.db import Db
from backend import workers
import os

port = int(os.environ.get('PORT', 5000))

app = None
cors = None
celery = None
mail = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'FlaskCard@gmail.com'
    app.config['MAIL_PASSWORD'] = '@flashcard00'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    cors = CORS(app)
    mail = Mail(app)
    db.init_app(app)
    app.app_context().push()
    celery = workers.celery
    celery.conf.update(
        broker_url = app.config["CELERY_BROKER_URL"],
        result_backend = app.config["CELERY_RESULT_BACKEND"]
    )
    celery.Task = workers.ContextTask
    app.app_context().push()
    return app,cors,celery,mail
    
app,cors,celery,mail = create_app()

from backend.api.user import *
from backend.api.deck import *
from backend.api.card import *
from backend.auth.auth import *

if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True, port = 33507)
