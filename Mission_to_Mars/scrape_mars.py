from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd  
import requests


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "C:/Users/misrael/Anaconda3/Scripts/chromedriver"}
    return Browser("chrome", **executable_path, headless= False)


def scrape():
    browser = init_browser()

    # Create mars data dictionary
    mars_data = {}

    # Visit nasa.com and grab html
    nasa_url = "https://mars.nasa.gov/news/"
    browser.visit(nasa_url)
    html = browser.html
    soup = bs(html, "html.parser")

    # Create soup object from html
    news_title= soup.find("div", class_="bottom_gradient").text
    news_p= soup.find("div", class_= "article_teaser_body").text

    # Add news title and paragraph to mars data
    mars_data["news_title"]= news_title
    mars_data["news_paragraph"]= news_p

    # Visit JPL page to get space image
    space_url= "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(space_url)
    html_image= browser.html
    soup= bs(html_image, "html.parser")

    # Create soup object from html
    image = soup.find("div", class_= "carousel_items").article["style"]

    # Splinter to find image url and parse out components
    image_url = image.split("/spaceimages")[-1].split(".")[0]

    # Set up featured image url
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages" + image_url + ".jpg"

    # Add image url to mars data
    mars_data["featured_image"]= featured_image_url

    # Visit space facts for mars facts
    mars_url= "https://space-facts.com/mars/"
    browser.visit(mars_url)
    html_table = browser.html
    soup = bs(html_table, "html.parser")

    # Create soup object from html
    mars_table= pd.read_html(mars_url)[0].rename(columns={0 : "Description", 1 : "Mars"}).set_index(["Description"])
    html_table = (mars_table.to_html()).replace('\n', '')

    # Add table info to mars data
    mars_data["mars_table"] = html_table

    # Visit astrogeology page for hemisphere info
    hemi_url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    html= browser.html
    soup= bs(html, "html.parser")

    # Create soup object to find all in item class
    items = soup.find_all('div', class_='item')

    # Set empty list and set homepage url
    hemisphere_image_urls = []

    hemispheres_url = "https://astrogeology.usgs.gov"

    # Loop through item class to get titles and urls
    for item in items: 
    
        title = item.find("h3").text
        
        image_url = item.find("a", class_="itemLink product-item")["href"]

        browser.visit(hemispheres_url + image_url)

        image_html = browser.html

        soup = bs(image_html, "html.parser")

        image_url = hemispheres_url + soup.find("img", class_="wide-image")["src"]
        
        hemisphere_image_urls.append({"Title" : title, "Image_URL" : image_url})

    # Add hemisphere info to mars data
    mars_data["hemispheres"]= hemisphere_image_urls

    browser.quit
    return mars_data

