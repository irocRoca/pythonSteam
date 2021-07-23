from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

PASS = 'cnt123'

@app.route('/')
def index():
    return render_template('base.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        password = request.form['password']
        if password == PASS:
            return render_template('home.html')
        else:
            return render_template('base.html', message='Inncorrect Password')

@app.route('/home', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        return render_template('home.html')
    else:
        return redirect(url_for('index'))

@app.route('/static_feed', methods=['POST', 'GET'])
def static_feed():
    if request.method == 'POST':
        return render_template('static.html')
    else:
        return redirect(url_for('index'))


@app.route('/live_feed',methods=['POST', "GET"])
def live_feed():
    if request.method == 'POST':
        return render_template('stream.html')
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)