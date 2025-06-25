from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

school_names= {'name': [],
                # 'location': [],
                # 'type': [],
                # 'conference': [], 
                }

# Set up Chrome options
options = Options()

# Automatically manages the ChromeDriver version
driver = webdriver.Chrome(options=options)

# Load the roster page
driver.get('https://www.ncsasports.org/mens-soccer/division-3-colleges')

# Wait for the page to fully load JS content
time.sleep(5)

# Get HTML after JavaScript renders
source = driver.page_source

driver.quit()

soup = BeautifulSoup(source, 'lxml')

for team in soup.find('section', class_='wp-block-ncsa-college-list').find_all('div', attrs={'class': 'row', 'itemprop': 'itemListElement'}):
    # get the name
    name = team.find('div', class_='container').a.text.strip()
    school_names['name'].append(name)

    # # get the location
    # location = team.find('div', itemprop='address').find('span', itemprop='addressLocality').text.strip()
    # location += ', ' + team.find('div', itemprop='address').find('span', itemprop='addressRegion').text.strip()
    # school_names['location'].append(location)


    # get the type
    # type = team.find('div', class_='container').find_all('div')[2].text.strip()
    # school_names['type'].append(type)

    # get the conference
    # conference = team.find('div', itemprop='member').text.strip()
    # school_names['conference'].append(conference)

import pandas as pd

# create the data frame to display the data in row/col
df=pd.DataFrame(school_names)

pd.set_option('display.max_rows', None)
print(df)

# create a csv file
df.to_csv('d3_schools_names.csv', index=False)