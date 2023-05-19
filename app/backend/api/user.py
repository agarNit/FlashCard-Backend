from flask import render_template, make_response
from flask import jsonify, request, url_for, redirect
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app as app
from marshmallow import ValidationError
from backend.db import Db
from backend.models import User, Card, Deck
from backend.errors import error_response
from backend.database import db
from functools import wraps
import jwt, pdfkit, os
from backend.api import deck
from flask_mail import Message, Mail
from backend import tasks
from pathlib import Path

mail = Mail(app)

def token_required(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		token = None
		# jwt is passed in the request header
		if 'x-access-token' in request.headers:
			token = request.headers['x-access-token']
		# return 401 if token is not passed
		if not token:
			return jsonify({'message' : 'Token is missing !!'}), 401

		try:
			# decoding the payload to fetch the stored details
			data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
			current_user = User.query.filter_by(public_id = data['public_id']).first()
		except:
			return jsonify({
				'message' : 'Token is invalid !!'
			}), 401
		# returns the current logged in users contex to the routes
		return f(current_user, *args, **kwargs)
		# return redirect(url_for('dashboard', username = current_user.username))

	return decorated

@app.route("/", methods = ['GET'])
def index():
    return jsonify("Welcome to the app")

@app.route("/user", methods=["GET"])
@token_required
def user(current_user):
	# querying the database
	# for all the entries in it
	user = current_user
	# converting the query objects
	# to list of jsons
	return jsonify({
        'id': user.id,
        'name' : user.username,
        'email' : user.email
    })

@app.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = Db.get_user(id)
    if user is None:
        return error_response(404)
    return user

@app.route("/users", methods=["POST"])
def create_user():
    try:
        user = request.json
    except ValidationError as err:
        return error_response(400, err.messages)
    if Db.get_user_by_email(email=user.get('email')):
        return error_response(400, "User already exists.")
    user = Db.add_user(user)
    if user is None:
        return error_response(400)
    response = jsonify(user=user)
    response.status_code = 201
    return response

@app.route('/<string:username>/signout')
def signout(username):
    user = db.session.query(User).filter(User.username == username).first()
    decks = db.session.query(Deck).filter(Deck.username == username).all()
    for deck in decks:
        cards = db.session.query(Card).filter(Card.deck_id == deck.deck_id).all()
        for card in cards:
            db.session.delete(card)
            db.session.commit()
        db.session.delete(deck)
        db.session.commit()
    db.session.delete(user)
    db.session.commit()
    return "Account deleted"
    
@app.route('/<string:username>/export')
def pdf_template(username):
    user = Db.get_user_by_name(username)
    # print(user.get('name'))
    decks = Db.all_decks_exported(user.get('name'))
    for deck in decks:
        deck_id = deck.get('deck_id')
        # print(deck_id)
        break
    cards = Db.all_cards_exported(deck_id)
    rendered = render_template('pdf.html', name=username, decks= decks, cards = cards, email=user.get('email'))
    pdf = pdfkit.from_string(rendered, False)
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=Output.pdf'
    
    return response

@app.route("/send/<string:username>", methods = ['GET'])
def send(username):
   user = Db.get_user_by_name(username)
   msg = Message('Report Generation', sender ='flaskcard@gmail.com',recipients = [user.get('email')])
   msg.body = 'Dear {}, Your report has been generated successfully !!'.format(user.get('name'))
   cd1 = str(os.path.join(Path.home(), "Downloads"))
   with app.open_resource("{}/{}.pdf".format(cd1, user.get('name'))) as fp:  
        msg.attach("{}.pdf".format(user.get('name')),"application/pdf",fp.read())  
        mail.send(msg)
   return 'Sent'
