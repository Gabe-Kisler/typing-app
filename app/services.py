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


def get_best_test (user_id, time):
    tests = db.collection('users').document(user_id).collection('tests').stream()
    best = None
    best_wpm = 0
    count = 0
    wpm_total = 0


    for test in tests:
        test_doc = test.to_dict()
        wpm = test_doc.get('gross_wpm', 0)
        test_time = test_doc.get('time', 0)


        if (time == test_time):


            if wpm > best_wpm:
                best = test_doc
                best_wpm = wpm


    return best        


def send_user_stats (user_id):
    total_test_taken = get_total_test_taken(user_id)
    fifteen_best = get_best_test (user_id, 15)


