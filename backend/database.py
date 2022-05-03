from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
import backend

engine = None
Base = declarative_base()
db = SQLAlchemy()