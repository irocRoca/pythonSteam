import os
import cv2
from flask import Flask, redirect, url_for, Response, render_template
from flask_dance.contrib.github import make_github_blueprint, github

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersekrit")
app.config["GITHUB_OAUTH_CLIENT_ID"] = os.environ.get("GITHUB_OAUTH_CLIENT_ID")
app.config["GITHUB_OAUTH_CLIENT_SECRET"] = os.environ.get("GITHUB_OAUTH_CLIENT_SECRET")
github_bp = make_github_blueprint()
app.register_blueprint(github_bp, url_prefix="/login")

@app.route("/")
def index():
    return render_template('base.html')

@app.route("/home")
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    resp = github.get("/user")
    assert resp.ok
    return render_template('home.html', login=resp.json()["login"])

@app.route('/video_feed')
def video_feed():
    return Response(generate(), mimetype = "multipart/x-mixed-replace; boundary=frame")

def generate():
    vs = cv2.VideoCapture(0)
    while True:

        ret, frame = vs.read()
        (flag, encodedImage) = cv2.imencode('.jpg', frame)

        if not flag:
            continue
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
			bytearray(encodedImage) + b'\r\n')




if __name__ == "__main__":
    app.run(threading=True)