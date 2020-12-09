from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
import scrape_mars
import os

# Create Flask
app = Flask(__name__)

mongo= PyMongo(app, uri="mongodb://localhost:27017/mars_app"

# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    mars_info = mongo.db.mars.find_one()
    return render_template("index.html", mars_info = mars_info)

# Route that will trigger the scrape function    
@app.route("/scrape")
def scrape():

    # Scrape function
    mars_info = mongo.db.mars_info
    data = scrape_mars.scrape()
    
    # Update the Mongo Database using update and upsert=True
    mars_info.update({}, data, upsert=True)
    
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
