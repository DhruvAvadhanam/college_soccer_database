from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

teamLinks = ['https://goairforcefalcons.com/sports/mens-soccer/roster', 'https://mgoblue.com/sports/mens-soccer/roster', 'https://bceagles.com/sports/mens-soccer/roster', 'https://athletics.bellarmine.edu/sports/mens-soccer/roster']

teams = ['Air Force', 'Michigan', 'Boston College', 'Bellarmine']
# iterate through the team names
i=0

# create empty dictionary with attributes
players_info = {'name': [],
                'team': [],
                'gradClass': [],
                'position': [], 
                'height': [],
                'weight': [], 
                'highSchool': [], 
                'homeTown_city': [],
                'homeTown_state': [] }

for link in teamLinks:
    # Set up Chrome options
    options = Options()

    # Automatically manages the ChromeDriver version
    driver = webdriver.Chrome(options=options)

    # Load the roster page
    driver.get(link)

    # Wait for the page to fully load JS content
    time.sleep(5)

    # Get HTML after JavaScript renders
    source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(source, 'lxml')

    players = soup.find('div', id='rosterListPrint').find_all('div', {'data-test-id': 's-person-card-list__root'})
    if len(players)==0:
        raise Exception('use other template')

    for player in players:
        player_data = {}
        # get the name
        name = player.find('div', class_='s-person-details__personal py-0.5').a.h3.text.strip()
        player_data['name']=name

        # assign the team
        player_data['team']=teams[i]

        try:
            otherInfo = player.find('div', 's-person-details__bio-stats s-text-details s-text-details-bold py-0.5').find_all('span', class_='s-person-details__bio-stats-item')
        except:
            otherInfo = player.find('div', 's-person-details__bio-stats s-text-details-bold py-0.5').find_all('span', class_='s-person-details__bio-stats-item')

        # print(otherInfo)

        # get the grad class
        try:
            gradClass = otherInfo[1].text.strip().split('Academic Year')[1].strip().split('.')[0]
        except:
            gradClass=None
        player_data['gradClass']=gradClass

        # get the position
        try:
            position = otherInfo[0].text.strip().split('Position')[1].strip()
        except:
            position = otherInfo[0].text.strip()
        player_data['position']=position

        # get the height
        try:
            height = otherInfo[2].text.strip().split('Height')[1].strip().split('\'\'')[0].replace(' ', '')
        except:
            height=None
        player_data['height']=height

        # get the weight
        try:
            weight = otherInfo[3].text.strip().split('Weight')[1].split('lbs')[0].strip()
        except:
            weight=None
        player_data['weight']=weight

        # get the high school
        try:
            highSchool = player.find('span', {'data-test-id': 's-person-card-list__content-location-person-high-school'}).text.strip().split('Last School')[1].strip()
        except:
            highSchool=None
        player_data['highSchool']=highSchool

        # get the home town
        try:
            homeTown_city = player.find('span', {'data-test-id': 's-person-card-list__content-location-person-hometown'}).text.strip().split('Hometown')[1].split(',')[0].strip()
        except:
            homeTown_city=None
        player_data['homeTown_city']=homeTown_city

        # get the home town
        try:
            homeTown_state = player.find('span', {'data-test-id': 's-person-card-list__content-location-person-hometown'}).text.strip().split('Hometown')[1].split(',')[1].strip()
        except:
            homeTown_state=None
        player_data['homeTown_state']=homeTown_state
        
        # put all the information in the dictionary
        for key in players_info:
            players_info[key].append(player_data.get(key, None))

    # iterate to the next team
    i += 1

import pandas as pd

# create the data frame to display the data in row/col
df=pd.DataFrame(players_info)

pd.set_option('display.max_rows', None)
print(df)


# create a csv file
# df.to_csv('emoryPlayers.csv', index=False)

