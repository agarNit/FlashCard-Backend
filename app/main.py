from flask import Flask, make_response, render_template
from backend.database import db
from backend.config import LocalDevelopmentConfig
from flask_cors import CORS
from flask_mail import Message, Mail
from backend.db import Db
import os

app = None
cors = None
mail = None

def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDevelopmentConfig)
    app.config['CORS_HEADERS'] = 'Content-Type'
    app.config['MAIL_SERVER']='smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = 'flaskcard@gmail.com'
    app.config['MAIL_PASSWORD'] = 'npdofnyaedsxqwex'
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    cors = CORS(app)
    mail = Mail(app)
    db.init_app(app)
    app.app_context().push()
    return app,cors,mail
    
app,cors,mail = create_app()

from backend.api.user import *
from backend.api.deck import *
from backend.api.card import *
from backend.auth.auth import *

@app.route("/")
def home_view():
        return "<h1>Welcome to home page</h1>"
    
if __name__=='__main__':
    app.run(host='127.0.0.1', debug=False)