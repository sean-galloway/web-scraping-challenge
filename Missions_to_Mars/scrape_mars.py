from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pandas as pd

def init_browser():
    # Setting up windows browser with chromedriver
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()

    mars_data = {}

    # -------------------------------------------------------------------
    # NASA Mars News
    # URL to scrape
    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)

    # Create BS Object, parse with html.parser
    soup = bs(response.text, 'html.parser')

    # Grab all of the Title Content
    results = soup.find_all('div', class_="content_title")
    # Set up a list
    news_titles = []
    # Loop over div elements
    for result in results:
        # Check for anchors
        if (result.a):
            # check for non-blank text
            if (result.a.text):
                # Append text to the list
                news_titles.append(result.a.text.strip())
    mars_data['news_title'] = news_titles[0]

    # Find the div for description paragraph below title
    p_results = soup.find_all('div', class_="rollover_description_inner")
    # Set up a list
    p_list = []
    for result in p_results:
        text = result.text.strip()
        p_list.append(text)
    mars_data['news_paragraph'] = p_list[0]

    # -------------------------------------------------------------------
    # JPL Mars Space Images - Featured Image
    # URL to scrape
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # HTML Text
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve background-image url from style tag
    featured_image_url = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url
    main_url = 'https://www.jpl.nasa.gov'

    # Concatenate website url with scrapped route
    featured_image_url = main_url + featured_image_url

    # Display full link to featured image
    mars_data['featured_image_url'] = featured_image_url

    # -------------------------------------------------------------------
    # Mars Facts
    url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to mars_df
    mars_df = mars_facts[0]

    # Assign the columns ['Description', 'Value']
    mars_df.columns = ['Description', 'Value']

    # Set the index to the Description
    mars_df.set_index('Description', inplace=True)

    # print out the html of the facts
    mars_data['html_table'] = mars_df.to_html()

    # -------------------------------------------------------------------
    # Need to use splinter since there are click throughs
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # HTML Object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for urls
    image_urls = []

    # Store the main_url
    main_url = 'https://astrogeology.usgs.gov'

    # Loop through the items previously stored
    for item in items:
        # Store title
        title = item.find('h3').text

        # Store link that leads to full image website
        img_url = item.find('a', class_='itemLink product-item')['href']

        # Visit the link that contains the full image website
        browser.visit(main_url + img_url)

        # HTML Object of individual hemisphere information website
        img_html = browser.html

        # Parse HTML with Beautiful Soup for every individual hemisphere information website
        soup = bs(img_html, 'html.parser')

        # Retrieve full image source
        img_url = main_url + soup.find('img', class_='wide-image')['src']

        # Append the retrieved information into a list of dictionaries
        image_urls.append({"title" : title, "img_url" : img_url})

    # Add the image_urls list to the mars_data dictionary
    mars_data['hemi_image_urls'] = image_urls

    return mars_data

# Call the scrape function if main
if __name__ == "__main__":
    scrape()