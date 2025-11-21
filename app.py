from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/location")
def location():
    return render_template("location.html")


@app.route("/entree-select")
def entree_select():
    return render_template("entree-select.html")


@app.route("/rate")
def rate():
    return render_template("rate.html")


@app.route("/menu")
def menu():
    return render_template("index.html")
    

@app.route("/reviews")
def reviews():
    return render_template("reviews.html")


@app.route("/about")
def about():
    return render_template("about.html")
