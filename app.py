#!/usr/bin/env python3
"""Basic Flask app"""

from flask import Flask, jsonify, request, abort
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound
import uuid

app = Flask(__name__)

AUTH = Auth()

@app.route("/", methods=['GET'], strict_slashes=False)
def basic():
    """basic route"""
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """Register user"""
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    phone_number = request.form.get('phone_number')
    address = request.form.get('address')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({
            "email": email,
            "message": "user created"
            })
    except ValueError as e:
        return jsonify({
            "message": "email already registered"
            }), 400
    
@app.route("/sessions", methods=['POST'], strict_slashes=False)   
def login():
    """Log in authorized user"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie('session_id', session_id)
            return response
                
        abort(401)
            
    except NoResultFound:
            abort(401)

@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """Delete session"""
    session_id = request.cookies.get('session_id')
    if session_id is None:
        abort(403)
    try:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
        abort(403)
    except NoResultFound:
        abort(403)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")

