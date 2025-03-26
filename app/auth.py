from flask import Blueprint, jsonify, request, redirect, url_for, session
from firebase_admin import auth
from .services import create_firebase_user


auth_bp = Blueprint ('auth_bp', __name__)

@auth_bp.route ('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']

        try :
            user = auth.get_user_by_email(email)
            session['user_id'] = user.uid
            return redirect(url_for('routes_bp.launch'))
        except Exception as e:
            print ('login failed, please try again', e)
            return redirect(url_for('routes_bp.index'))
    return redirect (url_for('routes_bp.index'))
   
@auth_bp.route ('/create-account', methods=['POST'])
def signup():

    print("Request content type:", request.content_type)
    print("Request data:", request.data)

    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 415
    
    try:
        user_data = request.get_json()
    except Exception as e:
        return jsonify({'error': 'Invalid JSON'}), 400
    
    username = user_data.get('username')
    email = user_data.get('email')
    password = user_data.get('password')


    if not all ([username, email, password]):
        return jsonify ({'message': 'please fill all required fields'})
   
    try:
        user = create_firebase_user(username, email, password)
        return jsonify({'message': 'account created'})
    except Exception as e:
        return jsonify({'message': 'could not create account', 'error': str(e)})
