from flask import Blueprint, render_template, request, jsonify, session
from .services import load_words_from_csv, get_total_test_taken, store_stats, get_best_test, get_average_tests, get_total_time_typing, get_tests




routes_bp = Blueprint ('routes_bp', __name__)
@routes_bp.route('/')
def index():
    return render_template ('index.html')




@routes_bp.route('/launch')
def launch():
    return render_template('launch.html')


@routes_bp.route('/stats-render')
def render_stats():
    return render_template('stats.html')




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
def store_user_stats ():
    user_id = session.get('user_id')
    data = request.get_json()


    print (data)


    net_wpm = data.get('netWPM')
    gross_wpm = data.get('grossWPM')
    errors = data.get('errors')
    time = data.get('time')
    difficulty = data.get('difficulty')


    test_taken = get_total_test_taken(user_id, None) + 1
    test_id = store_stats(user_id, test_taken, net_wpm, gross_wpm, errors, time, difficulty)
    return jsonify ({'succesfully stored test, tes_id:':test_id})


@routes_bp.route('/retrieve-stats', methods=['POST'])
def get_user_stats ():
    user_id = session.get('user_id')
    tests = get_tests (user_id)


    total_tests = get_total_test_taken(None, tests)
    typing_time = get_total_time_typing(tests)
    best_ovr_wpm = get_best_test (None, tests)
    fifteen_sec_best = get_best_test (15, tests)
    fifteen_sec_avg = get_average_tests (15, tests)
    fifteen_sec_tests = get_total_test_taken (15, tests)
    thirty_sec_best = get_best_test (30, tests)
    thirty_sec_avg = get_average_tests (30, tests)
    thirty_sec_tests = get_total_test_taken (30, tests)
    sixty_sec_best = get_best_test (60, tests)
    sixty_sec_avg = get_average_tests (60, tests)
    sixty_sec_tests = get_total_test_taken (60, tests)


    return jsonify ({
        'total_tests': total_tests,
        'typing_time': typing_time,
        'best_ovr_wpm': best_ovr_wpm,
        'fifteen_sec_best': fifteen_sec_best,
        'fifteen_sec_avg': fifteen_sec_avg,
        'fifteen_sec_tests': fifteen_sec_tests,
        'thirty_sec_best': thirty_sec_best,
        'thirty_sec_avg': thirty_sec_avg,
        'thirty_sec_tests': thirty_sec_tests,
        'sixty_sec_best': sixty_sec_best,
        'sixty_sec_avg': sixty_sec_avg,
        'sixty_sec_tests': sixty_sec_tests
    })














