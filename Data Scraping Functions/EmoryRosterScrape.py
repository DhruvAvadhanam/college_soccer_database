from bs4 import BeautifulSoup

import requests

# source = HTML of the website
source = requests.get('https://emoryathletics.com/sports/mens-soccer/roster').text

soup = BeautifulSoup(source, 'lxml')

# create empty dictionary with attributes
players_info = {'name': [],
                'gradClass': [],
                'position': [], 
                'height': [], 
                'weight': [], 
                'highSchool': [], 
                'homeTown': [] }


for player in soup.find_all('div', class_='sidearm-roster-player-container'):
    # get the name
    name = player.find('div', class_='sidearm-roster-player-name').h3.a.text
    # print(name)
    players_info['name'].append(name)

    # get the grad class
    gradClass = player.find('span', class_='sidearm-roster-player-academic-year').text.strip().split('.')[0]
    # print(gradClass)
    players_info['gradClass'].append(gradClass)

    # get the position
    position = player.find('div', class_='sidearm-roster-player-position').find('span', class_='text-bold').text.strip()
    # print(position)
    players_info['position'].append(position)

    try:
        # get the height
        height = player.find('div', class_='sidearm-roster-player-position').find('span', class_='sidearm-roster-player-height').text.strip().split('"')[0]
    except Exception as e:
        height = None

    # print(height)
    players_info['height'].append(height)

    try:
        # get the weight
        weight = player.find('div', class_='sidearm-roster-player-position').find('span', class_='sidearm-roster-player-weight').text.strip().split(' lbs')[0]    
    except Exception as e:
        weight = None
    
    # print(weight)
    players_info['weight'].append(weight)

    # get the high school
    highSchool = player.find('span', class_='sidearm-roster-player-highschool').text.strip()
    # print(highSchool)
    players_info['highSchool'].append(highSchool)

    # get the home town
    homeTown = player.find('span', class_='sidearm-roster-player-hometown').text.strip()
    # print(homeTown)
    players_info['homeTown'].append(homeTown)

    # print()

# print(players_info)

import pandas as pd

# create the data frame to display the data in row/col
df=pd.DataFrame(players_info)
print(df)


# heights = ['6\'0', '6\'1', '6\'2', '6\'3', '6\'4']

# filt = (df['height'] == '6\'0') & (df['position'] == 'M')

# filt2 = df['height'].isin(heights)


# print(df.loc[filt2])



# create a csv file
# df.to_csv('emoryPlayers.csv', index=False)

# print(df[['name', 'position']])
# print(df.columns)
# print(df.iloc[[0,1], 2])
# print(df.loc[0], 'name')
# print(df['position'].value_counts())
# print(df['gradClass'].value_counts())
# print (df)
