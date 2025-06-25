from bs4 import BeautifulSoup

import requests

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
                'homeTown': [] }

for link in teamLinks:
    # source = HTML of the website
    source = requests.get(link).text

    soup = BeautifulSoup(source, 'lxml')

    players=soup.find_all('div', class_='sidearm-roster-player-container')
    if len(players)==0:
        raise Exception('use other template')

    for player in players:
        # get the name
        name = player.find('div', class_='sidearm-roster-player-name').a.text
        players_info['name'].append(name)

        # assign the team
        players_info['team'].append(teams[i])

        # get the grad class
        gradClass = player.find('span', class_='sidearm-roster-player-academic-year').text.strip().split('.')[0]
        players_info['gradClass'].append(gradClass)

        # get the position
        try: 
            position = player.find('div', class_='sidearm-roster-player-position').find('span', class_='sidearm-roster-player-position-long-short hide-on-small-down').text.strip()
        except Exception as e:
            position = player.find('div', class_='sidearm-roster-player-position').find('span', class_='text-bold').text.strip()

        players_info['position'].append(position)

        try:
            # get the height
            height = player.find('div', class_='sidearm-roster-player-position').find('span', class_='sidearm-roster-player-height').text.strip().split('"')[0]
        except Exception as e:
            height = None

        players_info['height'].append(height)

        try:
            # get the weight
            weight = player.find('div', class_='sidearm-roster-player-position').find('span', class_='sidearm-roster-player-weight').text.strip().split(' lbs')[0]    
        except Exception as e:
            weight = None
        
        players_info['weight'].append(weight)

        # get the high school
        highSchool = player.find('span', class_='sidearm-roster-player-highschool').text.strip()
        players_info['highSchool'].append(highSchool)

        # get the home town
        homeTown = player.find('span', class_='sidearm-roster-player-hometown').text.strip()
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

