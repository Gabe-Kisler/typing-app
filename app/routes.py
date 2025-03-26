from flask import Blueprint, render_template, request, jsonify, session
from .services import load_words_from_csv, get_total_test_taken, store_stats


routes_bp = Blueprint ('routes_bp', __name__)
@routes_bp.route('/')
def index():
    return render_template ('index.html')


@routes_bp.route('/launch')
def launch():
    return render_template('launch.html')


@routes_bp.route ('/get-words', methods=['POST', 'GET'])
def get_words():
    level_choice = request.get_json().get('level')


    word_files = {
        "easy": 'app/static/resources/easyWords.csv',
        "medium": 'app/static/resources/mediumWords.csv',
        "hard": 'app/static/resources/hardWords.csv'
    }


    words_csv = word_files.get (level_choice, 'app/static/resources/easyWords.csv')
    random_words = load_words_from_csv (words_csv)


    return jsonify (wordsString=' '.join(random_words))

@routes_bp.route('/test-finished', methods=['POST'])
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





