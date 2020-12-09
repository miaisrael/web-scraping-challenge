from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data
    mars_data = mongo.db.mars_data.find_one()

    # Return template and data
    return render_template("index.html", mars = mars_data)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Scrape function
    mars_data = mongo.db.mars_data
    mars_scrape = scrape_mars.scrape()
    
    # Update the Mongo Database using update and upsert=True
    mars_data.update({}, mars_scrape, upsert=True)
    
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
