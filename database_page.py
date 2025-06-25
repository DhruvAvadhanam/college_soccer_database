from flask import Flask, render_template, request
import pandas as pd
import os

base_dir = os.path.dirname(os.path.abspath(__file__))  # gets folder where the Python script lives

app=Flask(__name__)

# # load csv into dataframe
# df = pd.read_csv('d1_players_filtered.csv')

@app.route("/")
def index():

    division = request.args.get('division', 'd1')
    if division == 'd3':
        df = pd.read_csv(os.path.join(base_dir, 'CSVs', 'd3_players_filtered.csv'))
    else:
        df = pd.read_csv(os.path.join(base_dir, 'CSVs', 'd1_players_filtered.csv'))

    team_filter=request.args.getlist('team')
    position_filter=request.args.getlist('position')
    grad_filter=request.args.getlist('gradClass')
    height_filter=request.args.getlist('height_group')
    weight_filter=request.args.getlist('weight_group')
    hometowncity_filter=request.args.getlist('homeTown_city')
    hometownstate_filter=request.args.getlist('region')

    filtered_df=df.copy()

    # filter the teams
    if team_filter and team_filter != 'All':
        filtered_df = filtered_df[filtered_df['team'].isin(team_filter)]
    
    if grad_filter and grad_filter != 'All':
        filtered_df = filtered_df[filtered_df['gradClass'].isin(grad_filter)]
    
    if position_filter and position_filter != 'All':
        filtered_df = filtered_df[filtered_df['position'].isin(position_filter)]
    
    if height_filter and height_filter != 'All':
        filtered_df = filtered_df[filtered_df['height_group'].isin(height_filter)]

    if weight_filter and weight_filter != 'All':
        filtered_df = filtered_df[filtered_df['weight_group'].isin(weight_filter)]
    
    if hometowncity_filter and hometowncity_filter != 'All':
        filtered_df = filtered_df[filtered_df['homeTown_city'].isin(hometowncity_filter)]
    
    if hometownstate_filter and hometownstate_filter != 'All':
        filtered_df = filtered_df[filtered_df['homeTown_state'].isin(hometownstate_filter)]

    teams = sorted(df['team'].dropna().unique())
    classes = sorted(df['gradClass'].dropna().unique())
    positions = sorted(df['position'].dropna().unique())
    heights = sorted(df['height_group'].dropna().unique())
    weights = sorted(df['weight_group'].dropna().unique())
    hometown_cities = sorted(df['homeTown_city'].dropna().unique())
    hometown_states = sorted(df['homeTown_state'].dropna().unique())

    return render_template('index.html', players=filtered_df.to_dict(orient='records'), teams=teams, classes=classes,
                           positions=positions, heights=heights, weights=weights, hometown_cities=hometown_cities,
                           hometown_states=hometown_states)

@app.route('/teams')
def teams():
    division = request.args.get('division', 'd1')
    if division == 'd3':
        df = pd.read_csv(os.path.join(base_dir, 'CSVs', 'd3_players_filtered.csv'))
        df2 = pd.read_csv(os.path.join(base_dir, 'CSVs', 'd3_teams_links_numbers.csv'))
    else:
        df = pd.read_csv(os.path.join(base_dir, 'CSVs', 'd1_players_filtered.csv'))
        df2 = pd.read_csv(os.path.join(base_dir, 'CSVs', 'd1_teams_links_numbers.csv'))

    grouped_teams = df.groupby('team')
    team_data = {}

    for team, group in grouped_teams:
        positionCounts = group['position'].value_counts().to_dict()
        gradCounts = group['gradClass'].value_counts().to_dict()
        stateCounts = group['homeTown_state'].value_counts().to_dict()
        playerList = group.to_dict(orient='records')
        keyFacts = []
        rosterLink = df2[df2['name'] == team]['link'].values[0]
        
        for position, count in positionCounts.items():
            if count>7:
                keyFacts.append(f"{team} has {count} {position}s")
        
        for gradClass, count in gradCounts.items():
            if count>7:
                keyFacts.append(f"{team} has {count} {gradClass}s")

        for state, count in stateCounts.items():
            if count>6:
                keyFacts.append(f"{team} has {count} players from {state}")

        team_data[team] = {
            'positionCounts': positionCounts,
            'gradCounts': gradCounts,
            'stateCounts': stateCounts,
            'playerList': playerList,
            'keyFacts': keyFacts,
            'rosterLink': rosterLink
        }

    return render_template('teams.html', teams=team_data)


if __name__ == "__main__":
    app.run(debug=True)



