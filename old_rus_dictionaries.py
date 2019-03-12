from flask import Flask, render_template, url_for, redirect, request
import json

with open('data.json', 'r', encoding='utf-8') as f:
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
    query = query.upper()
    
    mapping1 = {a: а, b: б}
    mapping2 = {a: б, b: в}
    query1 = ''
    for letter in query:
        query1 += mapping1[letter]
    query2 = ''
    for letter in query:
        query2 += mapping2[letter]
    
    try:
        res = js[query1]['data_XI–XVII']
        return render_template('res.html', result=res)
    except KeyError:
        try:
            res = js[query2]['data_XI–XVII']
        except KeyError:
            return render_template('error.html', comment='There is no such entry')


if __name__ == '__main__':
    app.run(threaded=True)
