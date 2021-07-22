import os
# setting the environment variables for local testing / not used on deployment
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

from flask import Flask, redirect, url_for, render_template
from flask_dance.contrib.google import make_google_blueprint, google

app = Flask(__name__)

# setting up the environment variables
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = os.environ.get('OAUTHLIB_RELAX_TOKEN_SCOPE')
app.config['SECRET_KEY'] = 'mysecret'
app.config['GOOGLE_OAUTH_CLIENT_ID'] = os.environ.get('CLIENT_ID')
app.config['GOOGLE_OAUTH_CLIENT_SECRET'] = os.environ.get('CLIENT_SECRET')

# setting up the google blueprint & registring it
blueprint = make_google_blueprint(reprompt_consent=True, scope=['profile', 'email'])
app.register_blueprint(blueprint, url_prefix='/login')


@app.route('/')
def index():
    if google.authorized:
        resp = google.get('/oauth2/v3/userinfo')
        assert resp.ok, resp.text
        name = resp.json()['name']
        return render_template('home.html', name=name)
    else:
        return render_template('base.html')


@app.route('/static_feed')
def static_feed():
    if google.authorized:
        resp = google.get('/oauth2/v3/userinfo')
        assert resp.ok, resp.text
        name = resp.json()['name']
        return render_template('static.html', name=name)
    else:
        return redirect(url_for('index'))


@app.route('/live_feed')
def live_feed():
    if google.authorized:
        resp = google.get('/oauth2/v3/userinfo')
        assert resp.ok, resp.text
        name = resp.json()['name']
        return render_template('live_feed.html', name=name)
    else:
        return redirect(url_for('index'))

@app.route('/login/google')
def login():
    if not google.authorized:
        return render_template(url_for('google.login'))
    resp = google.get('/oauth2/v3/userinfo')
    assert resp.ok, resp.text
    name = resp.json()['name']

    return redirect('home.html', name=name)


if __name__ == '__main__':
    app.run(debug=True)