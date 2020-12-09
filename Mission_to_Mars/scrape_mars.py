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

    # Visit space facts for mars facts
    mars_url= "https://space-facts.com/mars/"
    browser.visit(mars_url)

    # Create soup object from html
    mars_table= pd.read_html(mars_url)[0].rename(columns={0 : "Description", 1 : "Mars"}).set_index(["Description"])
    html_table = (mars_table.to_html()).replace('\n', '')

    # Visit astrogeology page for hemisphere info
    main_url= "https://astrogeology.usgs.gov"
    hemi_url= "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemi_url)
    html= browser.html
    soup= bs(html, "html.parser")

    # Set up needed classes from inspection and empty list for dict
    all_hemispheres = soup.find("div", class_="collapsible results")
    mars_hemispheres = all_hemispheres.find_all("div", class_= "item") 
    hemisphere_image_urls = []
        
    # Loop through hemispheres
    for i in mars_hemispheres:
        # Collect Title
        hemisphere = i.find("div", class_="description")
        title = hemisphere.h3.text        
        
        # Collect image link by browsing to hemisphere page
        hemisphere_link = hemisphere.a["href"]    
        browser.visit(main_url + hemisphere_link)        
        image_html = browser.html
        image_soup = bs(image_html, "html.parser")        
        image_link = image_soup.find("div", class_="downloads")
        image_url = image_link.find("li").a["href"]
        
        # Create dictionary to store title and url info and append to list
        image_dict = {}
        image_dict["title"] = title
        image_dict["image_url"] = image_url        
        hemisphere_image_urls.append(image_dict)


    # Create dictionary
    mars_data= {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "html_table": str(html_table),
        "hemisphere_images": hemisphere_image_urls
    }

    return mars_data

