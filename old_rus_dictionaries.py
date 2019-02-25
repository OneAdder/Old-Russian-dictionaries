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
    try:
        query = query.upper()
        res = js[query]['data_XI–XVII']
        # word = res[lexeme_XI–XVII]
        # descr = res[Full]
        return render_template('res.html', result=res)
    except KeyError:
        return render_template('error.html', comment='There is no such entry')


if __name__ == '__main__':
    app.run(threaded=True)
