from flask import jsonify, request, url_for
from flask import current_app as app
from backend.db import Db
from marshmallow import ValidationError
from backend.models import Deck, Card
from backend.errors import error_response
from backend.database import db
import jwt
import datetime as dt

@app.route('/<string:username>/dashboard', methods = ['GET'])
def dashboard(username):
    decks = Db.all_decks(username)
    # dee = Db.all_decks_exported(username)
    print(decks)
    if decks is None:
        return "No decks found"
    return decks

@app.route('/<string:username>/dashboard', methods = ['POST'])
def add_deck(username):
    try:
        deck = request.json
    except ValidationError as err:
        return error_response(400, err.messages)
    print(deck.get('deck_name'))
    if (deck.get('deck_name') == None):
        return error_response(400, "Enter deck name.")
    if Db.get_deck_by_name(username=username, deck_name=deck.get('deck_name')):
        return error_response(400, "Deck already exists.")
    new_deck = Db.add_deck(deck)
    if new_deck is None:
        return error_response(400)
    add_deck = Deck(deck_id = new_deck.get('deck_id'), username = username, deck_name = deck.get('deck_name'), deck_score = deck.get('deck_score'), deck_last_review_time = (dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)).strftime("%d-%b-%Y at %H:%M"))
    db.session.add(add_deck)
    db.session.commit()
    response = jsonify(deck=new_deck)
    response.status_code = 201
    return response
    
@app.route('/<string:username>/dashboard/<string:deck_name>/update', methods = ['PUT'])
def update_deck(username, deck_name):
    try:
        deck = request.json
        print(deck)
    except ValidationError as err:
        return error_response(400, err.messages)
    if (deck.get('deck_name') == ''):
        return error_response(400, "Enter deck name.")
    if Db.get_deck_by_name(username=username, deck_name=deck_name) == None:
        return error_response(400, "Deck does not exist.")
    # old_deck = Db.get_deck_by_name(deck_name=deck_name)
    # print(old_deck)
    db.session.query(Deck).filter(Deck.deck_name == deck_name).update({Deck.deck_name : deck.get('deck_name')})
    db.session.commit()
    response = jsonify(deck=deck)
    response.status_code = 201
    return response

@app.route('/<string:username>/dashboard/<int:deck_id>/delete', methods = ['DELETE'])
def delete_deck(username, deck_id):
    # print("hii")
    # try:
    #     deck = request.json
    # except ValidationError as err:
    #     return error_response(400, err.messages)
    # print("hii")
    old_deck = db.session.query(Deck).filter(Deck.deck_id == deck_id).first()
    if not old_deck:
        return error_response(400, "Deck does not exist.")
    print(old_deck)
    cards = db.session.query(Card).filter(Card.deck_id == deck_id).all()
    for card in cards:
        db.session.delete(card)
        db.session.commit()
    db.session.delete(old_deck)
    db.session.commit()
    decks = Db.all_decks(username)
    # print(decks)
    if decks is None:
        return "No decks found"
    return decks

@app.route("/decks/<int:deck_id>/reset", methods = ['GET'])
def reset(deck_id):
    # try:
    #     deck = request.json
    # except ValidationError as err:
    #     return error_response(400, err.messages)
    response = Db.reset(deck_id = deck_id)
    return response