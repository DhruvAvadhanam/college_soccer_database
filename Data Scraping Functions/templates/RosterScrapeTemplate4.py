from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

teamLinks = ['http://ohiostatebuckeyes.com/sports/mens-soccer/roster', 'https://fightingirish.com/sports/msoc/roster/', 'https://uclabruins.com/sports/mens-soccer/roster']

teams = ['Ohio State', 'Notre Dame', 'UCLA']
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

    # test if the link fits template 4
    try:
        players = soup.find('div', class_='c-rosterpage__players').find('tbody').find_all('tr')
    except:
        players = soup.find('table', id='players-table').find('tbody').find_all('tr')

    if len(players)==0:
        raise Exception('use other template')

    for player in players:
        player_data = {}

        data = player.find_all('td')

        # get the name
        try:
            name = data[1].a.text.strip()
        except:
            name=player.find('th').text.strip()
        player_data['name']= name

        # assign the team
        player_data['team']= teams[i]

        for td in data:
            positions = {'GK', 'D', 'MF', 'F', 'Goalkeeper', 'Defender', 'Forward', 'Midfielder'}
            classes = {'Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate', 'Fr', 'So', 'Jr', 'Sr', 'Gr'}

            # try:
            #     weight=td.span.text.strip()
            #     int(weight)
            # except:
            #     weight='1'

            try:
                text = td.span.text.strip()
            except:
                text=td.text.strip()
            
            if any(year in text for year in classes):
                gradClass=text
                player_data['gradClass']=gradClass
            elif any(pos in text for pos in positions):
                position=text
                player_data['position']=position
            elif '\'' in text:
                height=text
                player_data['height']=height
            elif 'lbs' in text:
                weight = text
                player_data['weight']=weight
            elif ',' in text:
                homeTown_city=text.split(',')[0]
                player_data['homeTown_city']=homeTown_city
                homeTown_state=text.split(',')[1]
                player_data['homeTown_state']=homeTown_state
            elif 'High School' in text:
                highSchool=text.split('High School')[1]
                player_data['highSchool']=highSchool
            
        for key in players_info:
            if key not in player_data:
                player_data[key]=None
        
        # put all the information in the dictionary
        for key in players_info:
            players_info[key].append(player_data.get(key, None))
    i+=1

import pandas as pd

# create the data frame to display the data in row/col
df=pd.DataFrame(players_info)

pd.set_option('display.max_rows', None)
print(df)


# create a csv file
# df.to_csv('emoryPlayers.csv', index=False)

