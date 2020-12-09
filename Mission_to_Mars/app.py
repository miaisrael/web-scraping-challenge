from flask import Flask, render_template, redirect, request
from flask_pymongo import PyMongo
import scrape_mars

# Create Flask
app = Flask(__name__)

mongo= PyMongo(app, uri="mongodb://localhost:27017/mars_app"

# Route to render index.html template using data from Mongo
@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars = mars)

# Route that will trigger the scrape function    
@app.route("/scrape")
def scrape():

    # Scrape function
    mars = mongo.db.mars
    data = scrape_mars.scrape()
    
    # Update the Mongo Database using update and upsert=True
    mars.update({}, data, upsert=True)
    
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)