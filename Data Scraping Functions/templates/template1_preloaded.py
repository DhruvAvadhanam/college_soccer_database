from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

teamLinks = ['https://usdtoreros.com/sports/mens-soccer/roster']

teams = ['USD']
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

    # test if the link fits template 3
    players = soup.find_all('div', class_='sidearm-roster-player-container')
    if len(players)==0:
        raise Exception('use other template')

    for player in players:
        player_data = {}

        # get the name
        name = player.find('div', class_='sidearm-roster-player-name').a.text
        player_data['name']= name

        # assign the team
        player_data['team']= teams[i]


        # get the grad class
        try:
            gradClass = player.find('span', class_='sidearm-roster-player-academic-year').text.strip().split('.')[0]
            player_data['gradClass']=gradClass
        except Exception as e:
            player_data['gradClass']=None
            # print("failed to get grad class")

        # get the position
        try: 
            position = player.find('div', class_='sidearm-roster-player-position').find('span', class_='sidearm-roster-player-position-long-short hide-on-small-down').text.strip()
            player_data['position']=position
        except Exception as e:
            try:
                position = player.find('div', class_='sidearm-roster-player-position').find('span', class_='text-bold').text.strip()
                player_data['position']=position
            except:
                player_data['position']=None
                # print("failed to get position")

        try:
            # get the height
            height = player.find('div', class_='sidearm-roster-player-position').find('span', class_='sidearm-roster-player-height').text.strip().split('"')[0]
            player_data['height']=height
        except Exception as e:
            player_data['height']=None
            # print("failed to get height")

        try:
            # get the weight
            weight = player.find('div', class_='sidearm-roster-player-position').find('span', class_='sidearm-roster-player-weight').text.strip().split(' lbs')[0]    
            player_data['weight']=weight
        except Exception as e:
            player_data['weight']=None
            # print("failed to get weight")
        
        try:
            # get the high school
            highSchool = player.find('span', class_='sidearm-roster-player-highschool').text.strip()
            player_data['highSchool']=highSchool
        except Exception as e:
            player_data['highSchool']=None
            # print("failed to get highschool")

        # get the home town - city and state/country seperate 
        try:
            homeTown = player.find('span', class_='sidearm-roster-player-hometown').text.strip()
            homeTown_city = homeTown.split(',')[0].replace(',', '')
            homeTown_state= homeTown.split(',')[1]
            player_data['homeTown_city']=homeTown_city
            player_data['homeTown_state']=homeTown_state

        except Exception as e:
            player_data['homeTown']=None
            # print("failed to get home town")
        
        # put all the information in the dictionary
        for key in players_info:
            players_info[key].append(player_data.get(key, None))

import pandas as pd

# create the data frame to display the data in row/col
df=pd.DataFrame(players_info)

pd.set_option('display.max_rows', None)
print(df)


# create a csv file
# df.to_csv('emoryPlayers.csv', index=False)

