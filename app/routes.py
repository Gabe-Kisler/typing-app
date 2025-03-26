from flask import Blueprint, render_template, request, jsonify
import random
from .services import load_words_from_csv


routes_bp = Blueprint ('routes', __name__)
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


    words_csv = word_files.get (level_choice, 'static/resources/easyWords.csv')
    random_words = load_words_from_csv (words_csv)


    return jsonify (wordsString=' '.join(random_words))




