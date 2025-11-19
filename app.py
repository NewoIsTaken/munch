from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, Brian!</p>"

@app.route("/about")
def about():
	return "<p>About this project!</p>"
