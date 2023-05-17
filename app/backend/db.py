from flask import json, jsonify
from backend.models import User, Deck, Card
from backend.database import db
import backend
import uuid
from werkzeug.security import check_password_hash
import datetime as dt

class Database:
    def __init__(self, app=None):
        self.app = app
        self.users = []
        self.decks = []
        self.cards = []

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.teardown_appcontext(self.teardown)
        with open("data.json") as fp:
            data = json.load(fp)
            self.users = User.load(data["users"], many=True)
            self.decks = Deck.load(data["decks"], many=True)
            self.cards = Card.load(data["cards"], many=True)

    def teardown(self, exception):
        pass

# -----------------------User functions---------------------

    def all_users(self):
        users = db.session.query(User).all()
        output = []
        for user in users:
            # appending the user data json
            # to the response list
            output.append({
                'id': user.id,
                'name' : user.username,
                'email' : user.email
            })
        return jsonify({'users': output})
    
    def get_user(self, id):
        # lst = list(filter(lambda u: u.id == id, self.users))
        user = db.session.query(User).filter(User.id == id).first()
        if user is None:
            return None
        output = []
        output.append({
            'id': user.id,
            'name' : user.username,
            'email' : user.email
        })
        return output[0]

    def get_user_by_name(self, name):
        user = db.session.query(User).filter(User.username == name).first()
        if user is None:
            return None
        output = []
        output.append({
            'id': user.id,
            'name' : user.username,
            'email' : user.email
        })
        # print(output[0])
        return output[0]
    
    def get_user_by_email(self, email):
        user = db.session.query(User).filter(User.email == email).first()
        # print(user)
        if user is None:
            return None
        output = []
        output.append({
            'id': user.id,
            'name' : user.username,
            'email' : user.email
        })
        return jsonify({'user': output})
     
    def check_credential(self, email, password):
        # print(email,password)
        user = db.session.query(User).filter(User.email == email).filter(User.password == password).first()
        if user is None:
            return None
        return user

    def get_next_user_id(self):
        users = db.session.query(User).all()
        if len(users) == 0:
            return 1
        return max([user.id for user in users]) + 1

    def add_user(self, user):
        if user is None:
            return None
        # if self.get_user_by_name(user.get('name')):
        #     return None
        user['id'] = self.get_next_user_id()
        self.users.append(user)
        return user

# ----------------Deck functions----------------
    
    def all_decks(self, username):
        decks = db.session.query(Deck).filter(Deck.username==username).all()
        # print(decks)
        output = []
        for deck in decks:
            # appending the user data json
            # to the response list
            output.append({
                'deck_id': deck.deck_id,
                'deck_name' : deck.deck_name,
                'deck_score' : deck.deck_score,
                'deck_last_review_time' : deck.deck_last_review_time
            })
        print(output)
        
        if len(output) == 0:
            return None
        return jsonify({"decks" : output})
    
    def all_decks_exported(self, username):
        decks = db.session.query(Deck).filter(Deck.username==username).all()
        # print(decks)
        output = []
        for deck in decks:
            # appending the user data json
            # to the response list
            output.append({
                'deck_id': deck.deck_id,
                'deck_name' : deck.deck_name,
                'deck_score' : deck.deck_score,
                'deck_last_review_time' : deck.deck_last_review_time
            })
        return output
    
    def add_deck(self, deck):
        if deck is None:
            return None
        # if self.get_user_by_name(user.get('name')):
        #     return None
        deck['deck_id'] = self.get_next_deck_id()
        self.decks.append(deck)
        return deck
    
    def get_deck_by_name(self, username, deck_name):
        deck = db.session.query(Deck).filter(Deck.username == username).filter(Deck.deck_name == deck_name).first()
        # print(deck)
        if deck is None:
            return None
        output = []
        output.append({
                'deck_id': deck.deck_id,
                'deck_name' : deck.deck_name,
                'deck_score' : deck.deck_score,
                'deck_last_review_time' : deck.deck_last_review_time
            })
        # print(output[0])
        return output[0]
    
    def get_next_deck_id(self):
        decks = db.session.query(Deck).all()
        if len(decks) == 0:
            return 1
        return max([deck.deck_id for deck in decks]) + 1
    
    def reset(self, deck_id):
        cards = db.session.query(Card).filter(Card.deck_id == deck_id).all()
        deck = db.session.query(Deck).filter(Deck.deck_id == deck_id).first()
        deck.deck_score = 0
        deck.deck_last_review_time = (dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)).strftime("%d-%b-%Y at %H:%M")
        db.session.commit()
        for card in cards:
            card.card_score = 0
            db.session.commit()
        return "Deck reset"
    
# ----------------Card functions----------------

    def all_cards(self, deck_id):
        cards = db.session.query(Card).filter(Card.deck_id==deck_id).all()
        if cards is None:
            return None
        # print(decks)
        output = []
        for card in cards:
            # appending the user data json
            # to the response list
            output.append({
                'deck_id': card.deck_id,
                'card_id': card.card_id,
                'card_front' : card.card_front,
                'card_back' : card.card_back,
                'card_last_review_time' : card.card_last_review_time,
                'card_score': card.card_score,
                'state': card.state
            })
        # print(output)
        
        if len(output) == 0:
            return None
        return jsonify({"cards" : output})
    
    def all_cards_exported(self, deck_id):
        cards = db.session.query(Card).filter(Card.deck_id==deck_id).all()
        # print(decks)
        output = []
        for card in cards:
            # appending the user data json
            # to the response list
            output.append({
                'deck_id': card.deck_id,
                'card_id': card.card_id,
                'card_front' : card.card_front,
                'card_back' : card.card_back,
                'card_last_review_time' : card.card_last_review_time,
                'card_score': card.card_score,
                'state': card.state
            })
        return output
    
    def add_card(self, card):
        # card = db.session.query(Card).filter(Card.deck_id == deck_id).first()
        if card is None:
            return None
        # if self.get_user_by_name(user.get('name')):
        #     return None
        card['card_id'] = self.get_next_card_id()
        self.cards.append(card)
        return card
    
    def get_card_by_name(self, deck_id, card_front):
        card = db.session.query(Card).filter(Card.deck_id == deck_id).filter(Card.card_front == card_front).first()
        # print(deck)
        if card is None:
            return None
        output = []
        output.append({
                'deck_id': card.deck_id,
                'card_front' : card.card_front,
                'card_back' : card.card_back,
                'card_score' : card.card_score,
                'card_last_review_time' : card.card_last_review_time
            })
        # print(output[0])
        return output[0]
    
    def get_next_card_id(self):
        cards = db.session.query(Card).all()
        if len(cards) == 0:
            return 1
        return max([card.card_id for card in cards]) + 1
    
    def update_easy(self, card_id):
        card = db.session.query(Card).filter(Card.card_id == card_id).first()
        deck_id = card.deck_id
        old_score = card.card_score
        card.card_score = old_score + 3
        dt_India = (dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)).strftime("%d-%b-%Y at %H:%M")
        card.card_last_review_time = dt_India
        deck = db.session.query(Deck).filter(Deck.deck_id == deck_id).first()
        deck.deck_score = deck.deck_score + 3 
        deck.deck_last_review_time = card.card_last_review_time
        db.session.commit()
        return "Score updated"
    
    def update_medium(self, card_id):
        card = db.session.query(Card).filter(Card.card_id == card_id).first()
        deck_id = card.deck_id
        old_score = card.card_score
        card.card_score = old_score + 2
        dt_India = (dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)).strftime("%d-%b-%Y at %H:%M")
        card.card_last_review_time = dt_India
        deck = db.session.query(Deck).filter(Deck.deck_id == deck_id).first()
        deck.deck_score = deck.deck_score + 2
        deck.deck_last_review_time = card.card_last_review_time
        db.session.commit()
        return "Score updated"
    
    def update_difficult(self, card_id):
        card = db.session.query(Card).filter(Card.card_id == card_id).first()
        deck_id = card.deck_id
        old_score = card.card_score
        card.card_score = old_score + 1
        dt_India = (dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)).strftime("%d-%b-%Y at %H:%M")
        card.card_last_review_time = dt_India
        deck = db.session.query(Deck).filter(Deck.deck_id == deck_id).first()
        deck.deck_score = deck.deck_score + 1
        deck.deck_last_review_time = card.card_last_review_time
        db.session.commit()
        return "Score updated"
    
    
Db = Database()