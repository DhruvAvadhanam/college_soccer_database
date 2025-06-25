from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

teamLinks = ['athletics.cmu.edu/', 'haverfordathletics.com']

teams = ['Carnegie Mellon', 'Haverford']
# iterate through the team names
i=0

# create empty dictionary with attributes
players_info = {'name': [],
                'team': [],
                'gradClass': [],
                'position': [], 
                'height': [], 
                'highSchool': [], 
                'homeTown': [] }

for link in teamLinks:
    # Set up Chrome options
    options = Options()

    # Automatically manages the ChromeDriver version
    driver = webdriver.Chrome(options=options)

    # Load the roster page
    driver.get('https://' + link + '/sports/msoc/2024-25/roster')

    # Wait for the page to fully load JS content
    time.sleep(5)

    # Get HTML after JavaScript renders
    source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(source, 'lxml')

    for player in soup.find('div', class_='roster-data style-list').find('tbody').find_all('tr'):
        # get the name
        name = player.find('th', {'scope': 'row', 'class': 'text-inherit'}).a.text.strip()
        name=' '.join(name.split())
        players_info['name'].append(name)

        # assign the team
        players_info['team'].append(teams[i])

        otherInfo = player.find_all('td', class_='text-nowrap')

        # get the grad class
        gradClass = otherInfo[2].text.split(':')[1].strip()
        players_info['gradClass'].append(gradClass)

        # get the position
        position = otherInfo[1].text.split(':')[1].strip().split('.')[0]
        players_info['position'].append(position)

        # get the height
        height = otherInfo[3].text.split(':')[1].strip()
        players_info['height'].append(height)

        # get the high school
        highSchool = player.find_all('td', class_='text-inherit')[1].text.strip().split(':')[1].strip().split('/')[1].strip()
        # highSchool = player.find('td', class_='text-inherit').text.strip().split('/')[1].strip()
        players_info['highSchool'].append(highSchool)

        # get the home town
        homeTown = player.find_all('td', class_='text-inherit')[1].text.strip().split(':')[1].strip().split('/')[0].strip()
        players_info['homeTown'].append(homeTown)

    # iterate to the next team
    i += 1

import pandas as pd

# create the data frame to display the data in row/col
df=pd.DataFrame(players_info)

pd.set_option('display.max_rows', None)
print(df)


# create a csv file
# df.to_csv('emoryPlayers.csv', index=False)

