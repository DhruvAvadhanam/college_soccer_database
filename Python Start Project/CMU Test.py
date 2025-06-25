from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

# df = pd.read_csv('d1_teams_links.csv')

teamLinks = ['https://athletics.cmu.edu/sports/msoc/2024-25/roster', 'https://www.haverfordathletics.com/sports/msoc/2024-25/roster', 'https://uclabruins.com/sports/mens-soccer/roster']
teams = ['CMU', 'Haverford', 'UCLA']

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
                'homeTown': [] }

for link in teamLinks:
    try:
        # source = HTML of the website
        source = requests.get(link).text

        soup = BeautifulSoup(source, 'lxml')

        # test if the link fits template 1
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
                print("failed to get grad class")

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
                    print("failed to get position")

            try:
                # get the height
                height = player.find('div', class_='sidearm-roster-player-position').find('span', class_='sidearm-roster-player-height').text.strip().split('"')[0]
                player_data['height']=height
            except Exception as e:
                player_data['height']=None
                print("failed to get height")

            try:
                # get the weight
                weight = player.find('div', class_='sidearm-roster-player-position').find('span', class_='sidearm-roster-player-weight').text.strip().split(' lbs')[0]    
                player_data['weight']=weight
            except Exception as e:
                player_data['weight']=None
                print("failed to get weight")
            
            try:
                # get the high school
                highSchool = player.find('span', class_='sidearm-roster-player-highschool').text.strip()
                player_data['highSchool']=highSchool
            except Exception as e:
                player_data['highSchool']=None
                print("failed to get highschool")

            # get the home town - city and state/country seperate 
            try:
                homeTown = player.find('span', class_='sidearm-roster-player-hometown').text.strip()
                homeTown_city = homeTown.split(',')[0].replace(',', '')
                homeTown_state= homeTown.split(',')[1]
                player_data['homeTown_city']=homeTown_city
                player_data['homeTown_state']=homeTown_state

            except Exception as e:
                player_data['homeTown']=None
                print("failed to get home town")
            
            # put all the information in the dictionary
            for key in players_info:
                players_info[key].append(player_data.get(key, None))

        print (f'{teams[i]} used template 1')
        # iterate to the next team
        i += 1
    except:
        try:
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

            # check if template 2 matches the link
            players=soup.find('div', class_='roster-data style-list').find('tbody').find_all('tr')
            if len(players)==0:
                raise Exception ('no templates work')

            for player in players:
                player_data = {}

                # get the name
                try:
                    name = player.find('th', {'scope': 'row', 'class': 'text-inherit'}).a.text.strip()
                    name=' '.join(name.split())
                    player_data['name']=name
                except Exception as e:
                    player_data['name']=None
                    print("failed to get name")

                # assign the team
                players_info['team'].append(teams[i])

                try:
                    otherInfo = player.find_all('td', class_='text-nowrap')
                except Exception as e:
                    print("failed to get otherInfo")

                # get the grad class
                try:
                    gradClass = otherInfo[2].text.split(':')[1].strip()
                    player_data['gradClass']=gradClass
                except Exception as e:
                    player_data['gradClass']=None
                    print("failed to get grad class")

                # get the position
                try:
                    position = otherInfo[1].text.split(':')[1].strip().split('.')[0]
                    player_data['position']=position
                except Exception as e:
                    print("failed to get position")
                    player_data['position']=None

                # get the height
                try:
                    height = otherInfo[3].text.split(':')[1].strip()
                    player_data['height']=height
                except Exception as e:
                    print("failed to get height")
                    player_data['heigt']=None

                # get the high school
                try:
                    highSchool = player.find_all('td', class_='text-inherit')[1].text.strip().split(':')[1].strip().split('/')[1].strip()
                    # highSchool = player.find('td', class_='text-inherit').text.strip().split('/')[1].strip()
                    player_data['highSchool']=highSchool
                except Exception as e:
                    print("failed to get highschool")
                    player_data['highSchool']=None

                # get the home town
                try:
                    homeTown = player.find_all('td', class_='text-inherit')[1].text.strip().split(':')[1].strip().split('/')[0].strip()
                    player_data['homeTown']=homeTown
                except Exception as e:
                    print("failed to get hometown")
                    player_data['homeTown']=None
                
                # put all the information in the dictionary
                for key in players_info:
                    players_info[key].append(player_data.get(key, None))

            print (f'{teams[i]} used template 2')
            # iterate to the next team
            i += 1
        except Exception as e:
            print(f'{teams[i]} failed both templates')
            i+=1


# create the data frame to display the data in row/col
df2=pd.DataFrame(players_info)

pd.set_option('display.max_rows', None)
print(df2)

# create a csv file
# df2.to_csv('d1_players.csv', index=False)