from flask import Blueprint
from flask import jsonify, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from backend.db import Db
from backend.models import User
from backend.errors import error_response
import uuid, jwt
from flask import current_app as app
from backend.database import db
from datetime import datetime, timedelta
from email_validator import validate_email, EmailNotValidError

@app.route('/signup', methods =['POST'])
def signup():
    # creates a dictionary of the form data
    user = request.json
    # print(user)
    if user.get('name') == "" or user.get('confirm_password') == "" or user.get('email') == "" or user.get('password') == "":
        return error_response(400, "Fill all details.")
    
    duplicate_name = Db.get_user_by_name(user.get('name'))
    if duplicate_name:
        return error_response(400, "Username already taken.")
    
    user_exist = Db.get_user_by_email(user.get('email'))
    if user_exist:
        return error_response(400, "Email already in use.")
    
    if user.get('password') != user.get('confirm_password'):
        return error_response(400, "Passwords do not match.")
    
    # print(user_exist)
    if not user_exist:
        # database ORM object
        new_user = Db.add_user(user)
        add_user = User(id = new_user.get('id'), public_id = str(uuid.uuid4()), username = user.get('name'), email = user.get('email'), password = user.get('password'))
        db.session.add(add_user)
        db.session.commit()
        return jsonify('Successfully registered.', 200)
    else:
        # returns 202 if user already exists
        # print("Enter different user.")
        return jsonify('Email already registered. Use a different email.', 202)
                             
@app.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return error_response(400)

    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_response(400, "Email or password missing.")

    user = Db.check_credential(email,password)
    if not user:
        return error_response(401, "Incorrect email or password.")
    token = jwt.encode({'public_id': user.public_id,'exp' : datetime.utcnow() + timedelta(minutes = 60)
            }, app.config['SECRET_KEY'])

    return jsonify({'token' : token }), 201
    # return redirect(url_for('token_required', token = token))
        # returns 403 if password is wrong

