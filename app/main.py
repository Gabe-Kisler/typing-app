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
        wordsCSV = 'static/resources/easyWords.csv'
    elif levelChoice == "medium":
        wordsCSV = 'static/resources/mediumWords.csv'
    elif levelChoice == 'hard':
        wordsCSV = 'static/resources/hardWords.csv'
    
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
        'username' : username,
        'email' : email,
    })
    return user

@app.route('/test-finished', methods=['POST'])
def get_stats ():
    user_id = session.get('user_id')
    data = request.get_json()

    print (data)

    net_wpm = data.get('netWPM')
    gross_wpm = data.get('grossWPM')
    errors = data.get('errors')
    time = data.get('time')
    difficulty = data.get('difficulty')

    test_taken = get_total_test_taken(user_id) + 1
    test_id = store_stats(user_id, test_taken, net_wpm, gross_wpm, errors, time, difficulty)
    return jsonify ({'succesfully stored test, tes_id:':test_id})





def store_stats (user_id, test_taken, net_wpm, gross_wpm, errors, time, difficulty):
    test = db.collection('users').document(user_id).collection('tests').document()
    test.set ({
        'test_taken' : test_taken,
        'net_wpm' : net_wpm,
        'gross_wpm' : gross_wpm,
        'errors' : errors,
        'time' : time,
        'difficulty' : difficulty,
        'timestamp': firestore.SERVER_TIMESTAMP
    })
    test_get_stats(user_id)
    return test.id


def test_get_stats (user_id):
    print (get_total_test_taken(user_id))
    print (get_average_gross_wpm(user_id))
    print (get_average_net_wpm(user_id))
    print (get_error_rate(user_id))

def get_total_test_taken (user_id):
    test_ref = db.collection('users').document(user_id).collection('tests')
    total_tests = len(list(test_ref.stream()))
    return total_tests


def get_average_gross_wpm (user_id):
    wpm_list = (db.collection('users').document(user_id).collection('tests').stream())

    wpm_total = 0
    count = 0

    for test in wpm_list:
        test_wpm = test.to_dict()
        wpm_total += test_wpm.get('gross_wpm', 0)
        count+=1

    if count > 0:
        average_gross_wpm = wpm_total / count
    else:
        average_gross_wpm = 0

    return average_gross_wpm    

def get_average_net_wpm (user_id):
    wpm_list = (db.collection('users').document(user_id).collection('tests').stream())

    wpm_total = 0
    count = 0

    for test in wpm_list:
        test_wpm = test.to_dict()
        wpm_total += test_wpm.get('net_wpm', 0)
        count += 1

    if count > 0:
        average_net_wpm = wpm_total / count
    else:
        average_net_wpm = 0

    return average_net_wpm    

def get_error_rate (user_id):
    error_list = (db.collection('users').document(user_id).collection('tests').stream())

    total_errors = 0
    count = 0

    for test in error_list:
        test_error = test.to_dict()
        total_errors += test_error.get('errors', 0)
        count += 1

        if total_errors > 0:
            average_error_per_test = total_errors / count
        else:
            average_error_per_test = 0    

    return average_error_per_test

def get_most_recent_tests (user_id):
    recent_tests = db.collection('users').document(user_id).collection('tests').limit(3).get()
    recent_tests_list = [test for test in recent_tests]

    if len(recent_tests_list) >= 3:
        return recent_tests_list[3].to_dict()
    elif len(recent_tests_list) == 2:
        return recent_tests_list[2].to_dict()
    elif len(recent_tests_list) == 1:
        return recent_tests_list[1].to_dict()
    else:
        return None

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

