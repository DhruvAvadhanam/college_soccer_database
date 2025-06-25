from bs4 import BeautifulSoup
import requests
import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

df = pd.read_csv('/Users/Dhruv/VScode/Python Start Project/CSVs/D3_teams_links_numbers.csv')

teamLinks = df['link']
teams = df['name']
template = df['template']

failedTeams=[]
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

    current_name = df.loc[i, 'name']
    current_template = df.loc[i, 'template']

    if pd.isna(current_template):
        try:
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
                player_data['team']= current_name

                for td in data:
                    positions = {'GK', 'D', 'MF', 'F', 'Goalkeeper', 'Defender', 'Forward', 'Midfielder'}
                    classes = {'Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate', 'Fr', 'So', 'Jr', 'Sr', 'Gr', 'Fy', 'Gs'}

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
        except:
            failedTeams.append(current_name)
            print(f'template failed for {current_name}')     
    
    i+=1



# create the data frame to display the data in row/col
df=pd.DataFrame(players_info)

# pd.set_option('display.max_rows', None)

print(df)
print(len(failedTeams))

# create a csv file
# df.to_csv('template6test.csv', index=False)

