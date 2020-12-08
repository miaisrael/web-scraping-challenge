from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager


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

    # Create soup object from html
    html_image= browser.html
    soup= bs(html_image, "html.parser")

    # Splinter to find image url and parse out components
    image = soup.find("div", class_= "carousel_items").article["style"]
    image_url = image.split("/spaceimages")[-1].split(".")[0]

    # Set up featured image url
    featured_image_url = "https://www.jpl.nasa.gov/spaceimages" + image_url + ".jpg"

    # Add image url to mars data
    mars_data["featured_image"]= featured_image_url

    # Visit space facts for mars facts
    mars_url= "https://space-facts.com/mars/"
    browser.visit(mars_url)

    