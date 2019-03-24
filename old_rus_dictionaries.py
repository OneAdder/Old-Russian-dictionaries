<<<<<<< HEAD
from flask import Flask, render_template, url_for, redirect, request
from flask_pymongo import PyMongo

=======
from flask import Flask, render_template, url_for, redirect, request, send_from_directory
>>>>>>> 66cddb83fd5b95ee5ce6837e3c83680d90e9a929
import json
import sys
import pyximport; pyximport.install()
sys.path.insert(0, './data_processing')
from unification import unify
__author__ = "Michael Voronov, Anna Sorokina"
__license__ = "GPLv3"

with open('data_processing/matched.json', 'r', encoding='utf-8') as f:
    js = json.loads(f.read())


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:33017/old_russian")

@app.route('/')
def index():
    return redirect(url_for('search'))

@app.route('/src/xi-xvii/pdf/Vol01ab/<pdf_name>')
def load_pdf(pdf_name):
    return send_from_directory('src/xi-xvii/pdf/Vol01ab', pdf_name)
    

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        qu = request.form['word']
        qu = qu.lower()
        query = unify(qu)
        try:
            res = js[query]
            return render_template('search.html', res=res)
        except KeyError: 
            return render_template('search.html', comment='There is no such entry')
    return render_template('search.html')

@app.route('/secret_search', methods=['GET', 'POST'])
def mongo_search():
    if request.method == 'POST':
        user_query = request.form['word']
        query = unify(user_query)
        if 'fourteen' in request.form:
            result = mongo.db.or_dictionaries.find_one({
                '$and': [
                    {'unified_lemma': query},
                    {'XVII_lemma': {'$exists': True}}
                ]
            })
        elif 'seventeen' in request.form:
            result = mongo.db.or_dictionaries.find_one({
                '$and': [
                    {'unified_lemma': query},
                    {'avanesov_lemma': {'$exists': True}}
                ]
            })
        elif 'verbs' in request.form:
            result = list(
                mongo.db.or_dictionaries.aggregate([
                    {'$match': {'avanesov_data.gramGrp': 'гл'}},
                    {'$match': {'unified_lemma': query}}
                ])
            )
        elif 'nouns' in request.args:
            result = list(
                mongo.db.or_dictionaries.aggregate([
                    {'$match': {'avanesov_data.gramGrp': 'с'}},
                    {'$match': {'unified_lemma': query}}
                ])
            )
        else:
            result = mongo.db.or_dictionaries.find_one({'unified_lemma': query})
        if result:
            return render_template('result.html', res=result)
        else: 
            return render_template('old_search.html', comment='There is no such entry')
    return render_template('old_search.html')

if __name__ == '__main__':
    app.run(threaded=True)
