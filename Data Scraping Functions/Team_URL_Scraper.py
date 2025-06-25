import pandas as pd
from googlesearch import search
import time
import csv

# Load the CSV with your school names
df = pd.read_csv('/Users/Dhruv/VScode/Python Start Project/CSVs/d3_schools_names.csv')

links = {'name': [], 'link': [] }

for school in df['name']:
    query = f"{school} men's soccer roster site"
    # print(f"Searching for: {query}")

    try:
        search_results = list(search(query, num_results=1))
        currentLink = search_results[0]
    except Exception as e:
        print(f"Error searching for {school}: {e}")
        link = "Error"
    
    links['name'].append(school)
    links['link'].append(currentLink)

    time.sleep(3)

# create the data frame to display the data in row/col
df2=pd.DataFrame(links)

pd.set_option('display.max_rows', None)
print(df2)

# create a csv file
# df2.to_csv('D3_teams_links.csv', index=False)

