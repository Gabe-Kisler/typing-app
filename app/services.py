import csv, random
from firebase_admin import firestore, auth


db = firestore.client()


def load_words_from_csv (csv_file):
    words = []
    with open (csv_file, mode='r', newline='') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            words.append(row[0])


        random_words = random.sample (words, 200)
        return random_words
   
def create_firebase_user (username, email, password):
    user = auth.create_user(email=email, password=password)
    db.collection('users').document(user.uid).set({'username':username, 'email':email})
    return user


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
    return test.id

def get_total_test_taken (user_id, time):
    total_tests = 0
    tests = db.collection('users').document(user_id).collection('tests').stream()

    if (time == None):
        total_tests = len(list(tests))
    elif (time != None):
        for test in tests:
            test_doc = test.to_dict()
            test_time = test_doc.get('time', 0)
            if int(time) == int(test_time):
                total_tests += 1
    return total_tests

def get_total_time_typing (user_id):
    tests = db.collection('users').document(user_id).collection('tests').stream()
    total_time = 0

    for test in tests:
        test_doc = test.to_dict()
        time = test_doc.get('time', 0)
        total_time += int(time)

    total_time_mins = round (total_time / 60, 2)
    return total_time_mins
    
def get_best_test (user_id, time):
    tests = db.collection('users').document(user_id).collection('tests').stream()
    best_wpm = 0

    if not tests:
        print ("no tests for user")

    for test in tests:
        test_doc = test.to_dict()
        wpm = test_doc.get('gross_wpm', 0)
        test_time = test_doc.get('time', 0)
        print (test_time, wpm)

        if (time == None):
            if int(wpm) > int(best_wpm):
                best_wpm = wpm
        
        elif int(time) == int(test_time):
            if int(wpm) > int(best_wpm):
                best_wpm = wpm


    return best_wpm 
  
def get_average_tests (user_id, time):
    tests = db.collection('users').document(user_id).collection('tests').stream()
    wpm_total = 0
    count = 0

    for test in tests:
        test_doc = test.to_dict()
        wpm = test_doc.get('gross_wpm', 0)
        test_time = test_doc.get('time', 0)

        if (time == None):
            wpm_total += wpm
            count += 1
        
        elif int(time) == int(test_time):
            wpm_total += wpm
            count += 1

    return round(wpm_total / count, 2) if count > 0 else 0


def send_user_stats (user_id):
    total_test_taken = get_total_test_taken(user_id)
    fifteen_best = get_best_test (user_id, 15)


