from flask import jsonify, request, url_for
from flask import current_app as app
from backend.db import Db
from marshmallow import ValidationError
from backend.models import Card
from backend.errors import error_response
from backend.database import db
import jwt
from flask_cors import cross_origin
import datetime as dt

@app.route('/<string:username>/<int:deck_id>/cards', methods = ['GET'])
def cards(username, deck_id):
    cards = Db.all_cards(deck_id)
    # print(cards)
    if cards is None:
        return "No cards found"
    # print(cards)
    return cards

@app.route('/<string:username>/<int:deck_id>/card', methods = ['POST'])
def add_card(username, deck_id):
    try:
        card = request.json
    except ValidationError as err:
        return error_response(400, err.messages)
    
    if (card.get('card_front') == '' or card.get('card_back') == ''):
        return error_response(400, "Empty field found")
    if Db.get_card_by_name(deck_id = deck_id, card_front=card.get('card_front')):
        return error_response(400, "Card already exists.")
    card = Db.add_card(card)
    if card is None:
        return error_response(400)
    new_card = Card(card_id = card.get('card_id'), deck_id = deck_id, card_front = card.get('card_front'), card_back = card.get('card_back'),card_score = card.get('card_score'), card_last_review_time = (dt.datetime.utcnow() + dt.timedelta(hours=5, minutes=30)).strftime("%d-%b-%Y at %H:%M"))
    db.session.add(new_card)
    db.session.commit()
    response = jsonify(card=card)
    response.status_code = 201
    return response
    
@app.route('/<int:deck_id>/<string:card_front>/update', methods = ['PUT'])
def update_card(deck_id, card_front):
    try:
        card = request.json
    except ValidationError as err:
        return error_response(400, err.messages)
    if (card.get('card_front') == '' or card.get('card_back') == ''):
        return error_response(400, "Empty field found") 
    if not Db.get_card_by_name(deck_id = deck_id, card_front=card_front):
        return error_response(400, "Card does not exist.")
    # print(old_deck)
    db.session.query(Card).filter(Card.card_front == card_front).update({Card.card_back : card.get('card_back')})
    db.session.query(Card).filter(Card.card_front == card_front).update({Card.card_front : card.get('card_front')})
    db.session.commit()
    response = jsonify(card=card)
    response.status_code = 201
    return response

@app.route('/<int:deck_id>/<string:card_front>/delete', methods = ['DELETE'])
def delete_card(deck_id,card_front):
    try:
        card = request.json
    except ValidationError as err:
        return error_response(400, err.messages)
    if not Db.get_card_by_name(deck_id = deck_id, card_front=card_front):
        return error_response(400, "Card does not exist.")
    old_card = db.session.query(Card).filter(Card.card_front == card_front).first()
    # print(old_deck)
    db.session.delete(old_card)
    db.session.commit()
    cards = Db.all_cards(deck_id)
    if cards is None:
        return "No cards found"
    print(cards)
    return cards

@app.route('/<int:deck_id>/cards/delete', methods = ['DELETE'])
def delete_cards(deck_id):
    try:
        card = request.json
    except ValidationError as err:
        return error_response(400, err.messages)
    cards = Db.all_cards(deck_id=deck_id)
    # print(old_deck)
    if cards is None:
        return "No cards found"
    db.session.delete(cards)
    db.session.commit()
    return "Cards deleted"

@app.route("/cards/<card_id>/easy", methods = ['GET'])
def easy(card_id):
    try:
        card = request.json
    except ValidationError as err:
        return error_response(400, err.messages)
    new_card = Db.update_easy(card_id=card_id)
    print(new_card)
    return new_card 

@app.route("/cards/<card_id>/medium", methods = ['GET'])
def medium(card_id):
    try:
        card = request.json
    except ValidationError as err:
        return error_response(400, err.messages)
    new_card = Db.update_medium(card_id=card_id)
    return new_card 

@app.route("/cards/<card_id>/difficult", methods = ['GET'])
def difficult(card_id):
    try:
        card = request.json
    except ValidationError as err:
        return error_response(400, err.messages)
    new_card = Db.update_difficult(card_id=card_id)
    return new_card 