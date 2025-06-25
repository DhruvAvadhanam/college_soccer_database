from bs4 import BeautifulSoup
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

teamLinks = ['http://ucfknights.com/sports/mens-soccer/roster/season/2025', 'https://gostanford.com/sports/mens-soccer/roster', 'https://gopsusports.com/sports/mens-soccer/roster']

teams = ['UCF', 'Stanford', 'Penn']
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
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    time.sleep(5)
    source = driver.page_source
    driver.quit()
    soup = BeautifulSoup(source, 'lxml')

    # test if the link fits template 4
    players = soup.find('div', class_='roster-players__group').find_all('div', class_='roster-card-item')
    print(f"{teams[i]} found {len(players)} players" )

    if len(players)==0:
        raise Exception('use other template')

    for player in players:
        player_data = {}

        data = player.find('div', class_='roster-card-item__content')
        if data is None:
            data = player.find('div', class_='roster-card-item__info')            

        # get the name
        name = data.a.text.strip()        
        player_data['name']= name

        # assign the team
        player_data['team']= teams[i]

        otherAtts = data.find('div', class_='roster-players-cards-item__profile-fields-wrapper').find_all('span')

        try:
            position = data.find('div', class_='roster-card-item__position').text.strip()
            player_data['position']=position
        except Exception as e:
            position=data.find('strong', class_='roster-card-item__position').text.strip()
            player_data['position']=position
        
        try:
            highSchool=data.find('span', class_='roster-player-card-profile-field__value roster-player-card-profile-field__value--school').text.strip()
            player_data['highSchool']=highSchool
        except Exception as e:
            highSchool=None

        for att in otherAtts:
            positions = {'GK', 'D', 'M', 'F', 'Goalkeeper', 'Defender', 'Forward'}
            classes = {'Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate'}

            try:
                gradClass=att.find('span', class_='profile-field-content__value').text.strip()
            except:
                gradClass=att.text.strip()

            if any(year in gradClass for year in classes):
                player_data['gradClass']=gradClass
            elif '′' in att.text.strip():
                height=att.text.strip().split('″')[0]
                player_data['height']=height
            elif 'lbs' in att.text.strip():
                weight = att.text.strip()
                player_data['weight']=weight
            elif ',' in att.text.strip():
                homeTown_city=att.text.strip().split(',')[0]
                player_data['homeTown_city']=homeTown_city
                homeTown_state=att.text.strip().split(',')[1]
                player_data['homeTown_state']=homeTown_state
            elif 'High School' in att.text.strip():
                highSchool=att.text.strip().split('High School')[1]
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

