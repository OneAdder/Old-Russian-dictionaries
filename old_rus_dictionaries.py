from flask import Flask, render_template, url_for, redirect, request
import json
import pyximport; pyximport.install()
from data_processing.unification import unify

__author__ = "Michael Voronov, Anna Sorokina"
__license__ = "GPLv3"

with open('data_processing/matched.json', 'r', encoding='utf-8') as f:
    js = json.loads(f.read())

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('search'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        qu = request.form['word']
        return redirect(url_for('search_result', query=qu))
    return render_template('search.html')

@app.route('/res/<query>')
def search_result(query):
    query = query.lower()
    query = unify(query)

    try: 
        res = js[query]
        return render_template('res.html', res=res)
    except KeyError: 
        return render_template('error.html', comment='There is no such entry')

""" 
# бывший поиск по avanesov.json
    for entry in js:
        if entry['unified_lemma'] == query:
            return render_template('res.html', res=entry)"""

if __name__ == '__main__':
    app.run(threaded=True)
