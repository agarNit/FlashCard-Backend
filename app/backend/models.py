from marshmallow import Schema, fields, post_load, validate
from backend.database import db
import datetime as dt
    
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key = True)
    public_id = db.Column(db.String(50), unique = True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(70), unique = True)
    password = db.Column(db.String(80))
    
    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)
    
class Deck(db.Model):
    __tablename__ = 'Deck'
    deck_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    username = db.Column(db.String, db.ForeignKey("User.username"))
    deck_name = db.Column(db.String)
    deck_score = db.Column(db.Float, default = 0)
    deck_last_review_time = db.Column(db.String, default = (dt.datetime.now()).strftime("%Y-%m-%d %H:%M"))
    
    @post_load
    def make_user(self, data, **kwargs):
        return Deck(**data)
    
class Card(db.Model):
    __tablename__ = 'Card'
    card_id = db.Column(db.Integer, autoincrement = True, primary_key = True)
    deck_id = db.Column(db.Integer, db.ForeignKey("Deck.deck_id"))
    card_front = db.Column(db.String)
    card_back = db.Column(db.String)
    card_score = db.Column(db.Float, default = 0)
    card_last_review_time = db.Column(db.String, default = (dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)).strftime("%d-%b-%Y at %H:%M"))
    state = db.Column(db.Integer, default = 0)
    
    @post_load
    def make_user(self, data, **kwargs):
        return Card(**data)