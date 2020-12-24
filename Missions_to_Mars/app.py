from flask import Flask, render_template, redirect, jsonify
from flask_pymongo import PyMongo
import scrape_mars
import sys

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    # Find mars_data
    mars_data = mongo.db.mars.find_one()
    # print(mars_data)
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scrape():
    # Grab the mars data from scrape_mars.py
    mars_scrape = scrape_mars.scrape()
    # Update mongo
    mongo.db.mars.update({}, mars_scrape, upsert=True)

    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)