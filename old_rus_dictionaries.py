from flask import Flask, render_template, url_for, redirect, request
import json

with open('data.json', 'r', encoding='utf-8') as f:
    js = json.load(f)

app = Flask(__name__)

@app.route('/')
def main_page():
    return redirect(url_for('search'))


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['word']
        return str(js[query])
    else:
        return render_template('search.html')

if __name__ == '__main__':
    app.run(threaded=True)
