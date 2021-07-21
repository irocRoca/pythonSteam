import os
import cv2

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


from flask import Flask, redirect, url_for, render_template, Response
from flask_dance.contrib.google import make_google_blueprint, google


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GOOGLE_OAUTH_CLIENT_ID"] = '384816377604-dhu0r6k2cg2ojfsonvbuqa2tcrkjdkkd.apps.googleusercontent.com'
app.config["GOOGLE_OAUTH_CLIENT_SECRET"] = '5wspr8oyOAKYmy7d15Pc2gQK'
google_bp = make_google_blueprint(scope=["profile", "email"])
app.register_blueprint(google_bp, url_prefix="/login")


@app.route('/')
def index():
    return render_template('base.html')

def generate():
    vs = cv2.VideoCapture(0)
    while True:

        ret, frame = vs.read()
        (flag, encodedImage) = cv2.imencode('.jpg', frame)

        if not flag:
            continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

@app.route('/home')
def home():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v1/userinfo")
    assert resp.ok, resp.text
    name = resp.json()["name"]
    return render_template('home.html', name=name)


if __name__ == "__main__":
    app.run(threading=True)