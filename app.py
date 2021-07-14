import os
import cv2
import threading



from flask import Flask, redirect, url_for, render_template, Response
from flask_dance.contrib.google import make_google_blueprint, google


vs = cv2.VideoCapture(0)
lock = threading.Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

blueprint = make_google_blueprint(client_id='384816377604-dhu0r6k2cg2ojfsonvbuqa2tcrkjdkkd.apps.googleusercontent.com', 
client_secret='5wspr8oyOAKYmy7d15Pc2gQK',
offline=True, scope=['profile', 'email'])

app.register_blueprint(blueprint,url_prefix='/login')




@app.route('/')
def index():
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/login/google')
def login():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    email = resp.json()['email']

    return render_template('home',email=email)


if __name__ == "__main__":
    app.run(threading=True)