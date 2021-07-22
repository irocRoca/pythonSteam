from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

PASS = '123456'
valid = False

@app.route('/')
def index():
    if valid:
        return render_template('home.html')
    else:
        return render_template('base.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        password = request.form['password']
        if password == PASS:
            global valid 
            valid = True
            return render_template('home.html')
        else:
            return render_template('base.html', message='wrong or empty password')

@app.route('/home')
def home():
    if valid:
        return render_template('home.html')
    else:
        return redirect(url_for('index'))

@app.route('/static_feed')
def static_feed():
    if valid:
        return render_template('static.html')
    else:
        return redirect(url_for('index'))


@app.route('/live_feed')
def live_feed():
    if valid:
        return render_template('stream.html')
    else:
        return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)