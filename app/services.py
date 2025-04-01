import csv, random, math
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


def get_tests (user_id):
    tests_ref = db.collection('users').document(user_id).collection('tests').stream()
    tests = []
    for test in tests_ref:
        tests.append (test.to_dict())


    print (" user tests: ", tests)
    return tests    


def get_total_test_taken (time, tests):
    total_tests = 0


    if (time == None):
        return len(tests)
    else:
        for test in tests:
            test_time = test.get('time', 0)
            if time == int(test_time):
                total_tests += 1
        return total_tests


def get_total_time_typing (tests):
    total_time = 0
    for test in tests:
        time = test.get('time', 0)
        total_time += int(time)
    total_time_secs = (total_time % 60)
    total_time_mins = math.floor(total_time / 60)


    return str(total_time_mins) + ":" + str(total_time_secs)
   
def get_best_test (time, tests):
    best_wpm = 0


    for test in tests:
        wpm = test.get('gross_wpm', 0)
        test_time = test.get('time', 0)


        if (time == None):
            if int(wpm) > best_wpm:
                best_wpm = float(wpm)
       
        elif time == int(test_time):
            if int(wpm) > best_wpm:
                best_wpm = float(wpm)




    return round (best_wpm, 1)
 
def get_average_tests (time, tests):
    wpm_total = 0
    count = 0


    for test in tests:
        wpm = test.get('gross_wpm', 0)
        test_time = test.get('time', 0)


        if (time == None):
            wpm_total += int(wpm)
            count += 1
       
        elif time == int(test_time):
            wpm_total += int(wpm)
            count += 1


    return round(wpm_total / count, 2) if count > 0 else 0




def send_user_stats (user_id):
    total_test_taken = get_total_test_taken(user_id)
    fifteen_best = get_best_test (user_id, 15)




