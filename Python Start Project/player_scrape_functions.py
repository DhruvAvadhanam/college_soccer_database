from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

df = pd.read_csv('/Users/Dhruv/VScode/Python Start Project/CSVs/d3_teams_links_numbers.csv')
# teamLinks = ['https://clemsontigers.com/sports/mens-soccer/roster/season/2024/']
# teams=['Clemson']
teams = df['name']
teamLinks = df['link']


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


def template1 (link, teamName):
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
            player_data['team']= teamName


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

def template2 (link, teamName):
    # Set up Chrome options
    options = Options()

    # Automatically manages the ChromeDriver version
    driver = webdriver.Chrome(options=options)

    # Load the roster page
    driver.get(link)

    # Wait for the page to fully load JS content
    time.sleep(1)

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
        player_data['team']=teamName

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

def template3 (link, teamName):
    # Set up Chrome options
    options = Options()

    # Automatically manages the ChromeDriver version
    driver = webdriver.Chrome(options=options)

    # Load the roster page
    driver.get(link)

    # Wait for the page to fully load JS content
    time.sleep(1)

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
        player_data['team']= teamName


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

def template4 (link, teamName):
    options = Options()
    driver = webdriver.Chrome(options=options)
    driver.get(link)
    time.sleep(1)
    source = driver.page_source
    driver.quit()
    soup = BeautifulSoup(source, 'lxml')

    # test if the link fits template 4
    players = soup.find('div', class_='roster-players__group').find_all('div', class_='roster-card-item')

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
        player_data['team']= teamName

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

def template5 (link, teamName):
    # Set up Chrome options
    options = Options()

    # Automatically manages the ChromeDriver version
    driver = webdriver.Chrome(options=options)

    # Load the roster page
    driver.get(link)

    # Wait for the page to fully load JS content
    time.sleep(1)

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
        name = data[1].a.text.strip()
        player_data['name']= name

        # assign the team
        player_data['team']= teamName

        # get the grad class
        try:
            gradClass = data[5].text.strip()
            player_data['gradClass']=gradClass
        except Exception as e:
            player_data['gradClass']=None
            # print("failed to get grad class")

        # get the position
        try: 
            position = data[2].text.strip()
            player_data['position']=position
        except Exception as e:
            player_data['position']=None
            # print("failed to get position")

        try:
            # get the height
            height = data[3].text.strip()
            player_data['height']=height
        except Exception as e:
            player_data['height']=None
            # print("failed to get height")

        try:
            # get the weight
            weight = data[4].text.strip()
            player_data['weight']=weight
        except Exception as e:
            player_data['weight']=None
            # print("failed to get weight")

        if '/' in data[7].text.strip():
            try:
                # get the high school
                highSchool = data[7].text.strip().split('/')[1]
                player_data['highSchool']=highSchool
            except Exception as e:
                player_data['highSchool']=None
            # print("failed to get highschool")
  
            # get the home town - city and state/country seperate if in col 7 
            try:
                homeTown = data[7].text.strip().split('/')[0]
                homeTown_city = homeTown.split(',')[0].replace(',', '')
                homeTown_state= homeTown.split(',')[1]
                player_data['homeTown_city']=homeTown_city
                player_data['homeTown_state']=homeTown_state

            except Exception as e:
                player_data['homeTown_city']=None
                player_data['homeTown_state']=None
                # print("failed to get home town")
        else:
            try:
                # get the high school
                highSchool = data[7].text.strip()
                player_data['highSchool']=highSchool
            except Exception as e:
                player_data['highSchool']=None
                # print("failed to get highschool")
     
            # get the home town - city and state/country seperate 
            try:
                homeTown = data[6].text.strip()
                homeTown_city = homeTown.split(',')[0].replace(',', '')
                homeTown_state= homeTown.split(',')[1]
                player_data['homeTown_city']=homeTown_city
                player_data['homeTown_state']=homeTown_state

            except Exception as e:
                player_data['homeTown_city']=None
                player_data['homeTown_state']=None
                # print("failed to get home town")
        
        # put all the information in the dictionary
        for key in players_info:
            players_info[key].append(player_data.get(key, None))

def template6 (link, teamName):
    # Set up Chrome options
    options = Options()

    # Automatically manages the ChromeDriver version
    driver = webdriver.Chrome(options=options)

    # Load the roster page
    driver.get(link)

    # Wait for the page to fully load JS content
    time.sleep(1)

    # Get HTML after JavaScript renders
    source = driver.page_source

    driver.quit()

    soup = BeautifulSoup(source, 'lxml')

    # test if the link fits template 6
    players = soup.find('tbody').find_all('tr')
    if len(players)==0:
        raise Exception('use other template')

    for player in players:
        player_data = {}

        data = player.find_all('td')

        # get the name
        name = player.find('th', scope='row').a.text.strip()
        name = " ".join(name.split())
        player_data['name']= name

        # assign the team
        player_data['team']= teamName

        for td in data:
            
            text = td.text.strip()
            text = " ".join(text.split())
            
            if 'Cl.:' in text:
                gradClass=text.split('Cl.:')[1].strip().split('.')[0]
                player_data['gradClass']=gradClass
            elif 'Pos.:' in text:
                position=text.split('Pos.:')[1].strip()
                player_data['position']=position
            elif 'Ht.:' in text:
                height=text.split('Ht.:')[1].strip()
                player_data['height']=height
            elif 'Wt.:' in text:
                weight=text.split('Wt.:')[1].strip()
                player_data['weight']=weight
            elif 'Hometown/High School' in text:
                try:
                    homeTown_city=text.split('Hometown/High School:')[1].split('/')[0].split(',')[0].strip()
                    homeTown_state=text.split('Hometown/High School:')[1].split('/')[0].split(',')[1].strip()
                except:
                    homeTown_city=text.split('Hometown/High School:')[1].split('/')[0]
                    homeTown_state=None

                highSchool=text.split('Hometown/High School')[1].split('/')[1].strip()

                player_data['homeTown_city']=homeTown_city
                player_data['homeTown_state']=homeTown_state
                player_data['highSchool']=highSchool
            elif 'Hometown:' in text:
                try:
                    homeTown_city = text.split('Hometown:')[1].split(',')[0].strip()
                    homeTown_state = text.split('Hometown:')[1].split(',')[1].strip()
                except:
                    homeTown_city = text.split('Hometown:')[1]
                    homeTown_state = None

                player_data['homeTown_city'] = homeTown_city
                player_data['homeTown_state'] = homeTown_state
            elif 'High School:' in text:
                highSchool = text.split('High School:')[1].strip()
                player_data['highSchool'] = highSchool

        for key in players_info:
            if key not in player_data:
                player_data[key]=None
        
        # put all the information in the dictionary
        for key in players_info:
            players_info[key].append(player_data.get(key, None))


failedTeams = []
i=0
# for link in teamLinks:
#     teamName=teams[i]
#     try:
#         template1(link,teamName)
#         df.loc[i, 'template']=1
#         print (f'{teamName} used template 1')
#         i += 1
#         continue
#     except Exception as e1:
#         try:
#             template2(link,teamName)
#             df.loc[i, 'template']=2
#             print (f'{teamName} used template 2')
#             i+=1
#             continue
#         except Exception as e2:
#             try:
#                 template3(link,teamName)
#                 df.loc[i, 'template']=3
#                 print (f'{teamName} used template 3')
#                 i+=1
#                 continue
#             except Exception as e3:
#                 try:
#                     template4(link,teamName)
#                     df.loc[i, 'template']=4
#                     print (f'{teamName} used template 4')
#                     i+=1
#                     continue
#                 except Exception as e4:
#                     try:
#                         template5(link,teamName)
#                         df.loc[i, 'template']=5
#                         print (f'{teamName} used template 5')
#                         i+=1
#                         continue
#                     except Exception as e5:
#                         try:
#                             template6(link,teamName)
#                             df.loc[i, 'template']=6
#                             print (f'{teamName} used template 6')
#                             i+=1
#                             continue
#                         except Exception as e6:
#                             print(f'all templates failed for {teamName}')
#                             df.loc[i, 'template']=None
#                             failedTeams.append(teamName)
#                             i+=1

for link in teamLinks:
    teamName=teams[i]
    template_number = df.loc[i, 'template']

    if template_number == 1:
        template1(link,teamName)
    elif template_number == 2:
        template2(link,teamName)
    elif template_number == 3:
        template3(link,teamName)
    elif template_number == 4:
        template4(link,teamName)
    elif template_number == 5:
        template5(link,teamName)
    elif template_number == 6:
        template6(link,teamName) 
    else:
        try:
            template6(link,teamName)
            df.loc[i, 'template']=6
        except:
            print(f'All templates failed for {teamName}')
            failedTeams.append(teamName)
    i+=1

# create the data frame to display the data in row/col
df2=pd.DataFrame(players_info)

# pd.set_option('display.max_rows', None)
print(df2)
print(failedTeams)
print(len(failedTeams))

# create a csv file for the players
df2.to_csv('d3_players.csv', index=False)

# create a new csv file for the teams
df.to_csv('d3_teams_links_numbers.csv', index=False)

