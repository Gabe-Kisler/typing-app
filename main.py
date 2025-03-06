from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import firebase_admin 
from firebase_admin import credentials, firestore, auth
import csv, random

app = Flask (__name__)
app.secret_key = 'secretKey'

cred = credentials.Certificate("credentials/Credentials.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def loadWordsFromCSV (csv_file):
    with open (csv_file, mode='r') as file:
        reader = csv.reader(file)
        words = [word for row in reader for word in row]
    return words

@app.route ('/get-words', methods=['POST', 'GET'])
def getWords ():
    levelChoice = request.get_json().get('level')
    if levelChoice == "easy" :
        wordsCSV = 'static/easyWords.csv'
    elif levelChoice == "medium":
        wordsCSV = 'static/mediumWords.csv'
    elif levelChoice == 'hard':
        wordsCSV = 'static/hardWords.csv'
    
    words = loadWordsFromCSV (wordsCSV)
    numWords = 200
    randomWords = random.sample (words, numWords)
    wordsString = ' '.join(randomWords)
    return jsonify(wordsString=wordsString)

@app.route('/')
def index():
    print ("index route hit")
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try :
            user = auth.get_user_by_email(email)
            session['user_id'] = user.uid
            return redirect(url_for('launch'))
        except Exception as e:
            print ('login failed, please try again')
            return redirect(url_for('index'))
    return redirect (url_for('index.html'))

@app.route('/create-account', methods=['POST'])
def create_account():
    
    user = request.get_json()

    
    username = user.get('username')
    email = user.get('email')
    password = user.get('password')

    if not username or not email or not password:
        return jsonify({'message': 'please fill all required fields'}), 400

    try:
        user = create_firebase_user (username, email, password)
        print ('account created successfully! please login')
        return jsonify({"message": "account created succesfully"}), 200 
    except Exception as e:
        print (f'could not create account: {e}')
        return jsonify({"message": f"could not create account: {str(e)}"}), 400  

def create_firebase_user (username, email, password):
    user = auth.create_user(email=email, password=password)
    db.collection('users').document(user.uid).set({
        'username':username
    })
    return user

def load_words ():
    words = []
    with open ('static/words.csv', mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            words.append(row[0])
    return words

@app.route('/launch')
def launch():
    return render_template('launch.html')

if __name__ == '__main__':
    app.run(debug=True)    

