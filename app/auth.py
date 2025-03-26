from flask import Blueprint, jsonify, request, redirect, url_for, session
from firebase_admin import auth
from .services import create_firebase_user


auth_bp = Blueprint ('auth_bp', __name__)
@auth_bp.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    try:
        user = auth.get_user_by_email(email)
        session['user_id'] = user.uid
        return redirect(url_for('routes_bp.launch'))
    except Exception as e:
        error = request.json.get('error', {}).get('message', 'unknown error')
        print (f"login failed: {error}")
        return jsonify({'message': 'login flailed'})
   
@auth_bp.route ('/create-account', methods=['POST'])
def signup():
    user_data = request.get_json()
    username = user_data.get('username')
    email = user_data.get('email')
    password = user_data.get('password')


    if not all [username, email, password]:
        return jsonify ({'message': 'please fill all required fields'})
   
    try:
        user = create_firebase_user(username, email, password)
        return jsonify({'message': 'account created'})
    except Exception as e:
        return jsonify({'message': 'could not create account'})
