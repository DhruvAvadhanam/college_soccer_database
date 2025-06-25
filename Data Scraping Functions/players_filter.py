import pandas as pd
import csv


# Load the CSV with your school names
df = pd.read_csv('/Users/Dhruv/VScode/Python Start Project/CSVs/d1_players.csv')

# map for graduating class
class_map = {
    'fr': 'Freshman',
    'fy': 'Freshman',
    'so': 'Sophomore',
    'jr': 'Junior',
    'sr': 'Senior',
    'rf': 'Redshirt Freshman',
    'r-fr': 'Redshirt Freshman',
    'rs so': 'Redshirt Sophomore',
    'r-so': 'Redshirt Sophomore',
    'r-jr': 'Redshirt Junior',
    'r-sr': 'Redshirt Senior',
    '5th': 'Graduate Student',
    '6th': 'Graduate Student',
    'gr': 'Graduate Student',
    'grad': 'Graduate Student'
}
df['gradClass'] = df['gradClass'].fillna('').str.lower().map(class_map)

# map for positions
position_map = {
    # Goalkeepers
    'gk': 'Goalkeeper',
    'goalkeeper': 'Goalkeeper',
    'goal keeper': 'Goalkeeper',
    'goaltender': 'Goalkeeper',
    'g': 'Goalkeeper',
    'gk is captain (c)': 'Goalkeeper',

    # Defenders
    'd': 'Defender',
    'def': 'Defender',
    'defense': 'Defender',
    'back': 'Defender',
    'b': 'Defender',
    'defender': 'Defender',
    'center back': 'Defender',
    'centerback': 'Defender',
    'left back': 'Defender',
    'outside back': 'Defender',
    'defender/center back': 'Defender',
    'defender // captain': 'Defender',
    'd is captain (c)': 'Defender',

    # Midfielders
    'm': 'Midfielder',
    'mf': 'Midfielder',
    'mid': 'Midfielder',
    'midfielder': 'Midfielder',
    'midfield': 'Midfielder',
    'central midfielder': 'Midfielder',
    'center midfielder': 'Midfielder',
    'left midfielder': 'Midfielder',
    'cam': 'Midfielder',
    'cm': 'Midfielder',
    'midfielder (captain)': 'Midfielder',
    'm is captain (c)': 'Midfielder',
    'midfielder // captain': 'Midfielder',

    # Forwards
    'f': 'Forward',
    'fwd': 'Forward',
    'forward': 'Forward',
    'winger': 'Forward',
    'striker': 'Forward',
    'foward': 'Forward',
    'wide forward': 'Forward',
    'wing': 'Forward',
    'winger / fwd': 'Forward',
    'winger / forward': 'Forward',
    'striker / winger': 'Forward',
    'attack': 'Forward',

    # Defender / Midfielder
    'defender / midfielder': 'Defender / Midfielder',
    'defender/midfielder': 'Defender / Midfielder',
    'defender/midfield': 'Defender / Midfielder',
    'defense/midfield': 'Defender / Midfielder',
    'defense/midfielder': 'Defender / Midfielder',
    'midfielder / defender': 'Defender / Midfielder',
    'midfielder/defender': 'Defender / Midfielder',
    'midfield/defender': 'Defender / Midfielder',
    'midfielder/defense': 'Defender / Midfielder',
    'midfield / defense': 'Defender / Midfielder',
    'midfield/defense (captain)': 'Defender / Midfielder',
    'd/m': 'Defender / Midfielder',
    'm/d': 'Defender / Midfielder',
    'd/mf': 'Defender / Midfielder',
    'mf/d': 'Defender / Midfielder',
    'mf/b': 'Defender / Midfielder',
    'back/midfield': 'Defender / Midfielder',

    # Midfielder / Forward
    'f/m': 'Midfielder / Forward',
    'm/f': 'Midfielder / Forward',
    'f/mf': 'Midfielder / Forward',
    'mf/f': 'Midfielder / Forward',
    'midfielder/forward': 'Midfielder / Forward',
    'midfield/forward': 'Midfielder / Forward',
    'midfielder/ forward': 'Midfielder / Forward',
    'forward / midfielder': 'Midfielder / Forward',
    'forward/midfielder': 'Midfielder / Forward',
    'forward / midfield': 'Midfielder / Forward',
    'forward/midfield': 'Midfielder / Forward',
    'winger / midfielder': 'Midfielder / Forward',
    'winger / midfield': 'Midfielder / Forward',
    'for./mid': 'Midfielder / Forward',
    'f/w': 'Midfielder / Forward',

    # Defender / Forward
    'defender/forward': 'Defender / Forward',
    'defender / forward': 'Defender / Forward',
    'forward / defender': 'Defender / Forward',
    'forward/defender': 'Defender / Forward',
    'defender/ winger': 'Defender / Forward',
    'defender/ mid': 'Defender / Midfielder',
    'f/b': 'Defender / Forward',
    'f/d is captain (c)': 'Defender / Forward',

    # Utility/Hybrid
    '12th man': '12th man',
    'utility': 'Utility',

    # Unknown/non-position values
    'academic year gr.': 'Unknown',
    'academic year fr.': 'Unknown',
    'academic year so.': 'Unknown',
    'academic year jr.': 'Unknown',
    'academic year sr.': 'Unknown',
    'freshman': 'Unknown',
    'nan': 'Unknown'
}
df['position']=df['position'].str.lower().map(position_map)  

# map for states
state_map = {
    # West Coast
    'wa': '(WA) - Washington',
    'wash.': '(WA) - Washington',
    'wash': '(WA) - Washington',
    'washington': '(WA) - Washington',

    'or': '(OR) - Oregon',
    'ore.': '(OR) - Oregon',
    'oreg.': '(OR) - Oregon',
    'oregon': '(OR) - Oregon',

    'ca': '(CA) - California',
    'calif.': '(CA) - California',
    'calif': '(CA) - California',
    'california': '(CA) - California',

    # Southwest
    'az': '(AZ) - Arizona',
    'ariz.': '(AZ) - Arizona',
    'arizona': '(AZ) - Arizona',

    'nm': '(NM) - New Mexico',
    'n.m.': '(NM) - New Mexico',
    'new mexico': '(NM) - New Mexico',

    'tx': '(TX) - Texas',
    'texas': '(TX) - Texas',
    'tex.': '(TX) - Texas',
    't.x.': '(TX) - Texas',
    'tx.': '(TX) - Texas',

    # Midwest
    'il': '(IL) - Illinois',
    'ill.': '(IL) - Illinois',
    'illi.': '(IL) - Illinois',
    'illinois': '(IL) - Illinois',

    'in': '(IN) - Indiana',
    'indiana': '(IN) - Indiana',

    'oh': '(OH) - Ohio',
    'oh.': '(OH) - Ohio',
    'ohio': '(OH) - Ohio',

    'mi': '(MI) - Michigan',
    'mich.': '(MI) - Michigan',
    'mich': '(MI) - Michigan',
    'michigan': '(MI) - Michigan',

    'mn': '(MN) - Minnesota',
    'minn.': '(MN) - Minnesota',
    'minnesota': '(MN) - Minnesota',

    'wi': '(WI) - Wisconsin',
    'wis.': '(WI) - Wisconsin',
    'wisc.': '(WI) - Wisconsin',
    'wisconsin': '(WI) - Wisconsin',

    'mo': '(MO) - Missouri',
    'mo.': '(MO) - Missouri',
    'missouri': '(MO) - Missouri',

    'ks.': '(KS) - Kansas',
    'ks': '(KS) - Kansas',
    'kan.': '(KS) - Kansas',
    'kansas': '(KS) - Kansas',

    'ne': '(NE) - Nebraska',
    'neb.': '(NE) - Nebraska',
    'nebraska': '(NE) - Nebraska',

    'ia': '(IA) - Iowa',
    'i.a.': '(IA) - Iowa',
    'iowa': '(IA) - Iowa',

    'nd': '(ND) - North Dakota',
    'north dakota': '(ND) - North Dakota',
    'sd': '(SD) - South Dakota',
    'south dakota': '(SD) - South Dakota',

    # Southeast
    'fl': '(FL) - Florida',
    'fla.': '(FL) - Florida',
    'florida': '(FL) - Florida',
    'f.l.': '(FL) - Florida',

    'ga': '(GA) - Georgia',
    'ga.': '(GA) - Georgia',
    'georgia': '(GA) - Georgia',
    'g.a.': '(GA) - Georgia',

    'al': '(AL) - Alabama',
    'ala.': '(AL) - Alabama',
    'alabama': '(AL) - Alabama',

    'sc': '(SC) - South Carolina',
    's.c.': '(SC) - South Carolina',

    'nc': '(NC) - North Carolina',
    'n.c.': '(NC) - North Carolina',

    'ms': '(MS) - Mississippi',
    'miss.': '(MS) - Mississippi',

    'la': '(LA) - Louisiana',
    'la.': '(LA) - Louisiana',
    'l.a.': '(LA) - Louisiana',

    'ky': '(KY) - Kentucky',
    'ky.': '(KY) - Kentucky',

    'tn': '(TN) - Tennessee',
    'tenn.': '(TN) - Tennessee',

    'ar': '(AR) - Arkansas',
    'ark.': '(AR) - Arkansas',

    'wv': '(WV) - West Virginia',
    'w.va.': '(WV) - West Virginia',
    'w.v.': '(WV) - West Virginia',

    'vir.': '(VA) - Virginia',


    # Northeast
    'ny': '(NY) - New York',
    'n.y.': '(NY) - New York',
    'new york': '(NY) - New York',

    'pa': '(PA) - Pennsylvania',
    'pa.': '(PA) - Pennsylvania',
    'p.a.': '(PA) - Pennsylvania',
    'penn.': '(PA) - Pennsylvania',

    'nj': '(NJ) - New Jersey',
    'n.j.': '(NJ) - New Jersey',
    'new jersey': '(NJ) - New Jersey',

    'ct': '(CT) - Connecticut',
    'conn.': '(CT) - Connecticut',

    'ma': '(MA) - Massachusetts',
    'mass.': '(MA) - Massachusetts',
    'mass': '(MA) - Massachusetts',

    'vt': '(VT) - Vermont',
    'vt.': '(VT) - Vermont',

    'ri': '(RI) - Rhode Island',
    'r.i.': '(RI) - Rhode Island',

    'nh': '(NH) - New Hampshire',
    'n.h.': '(NH) - New Hampshire',

    'me': '(ME) - Maine',
    'maine': '(ME) - Maine',

    # Mid-Atlantic
    'de': '(DE) - Delaware',
    'del.': '(DE) - Delaware',

    'md': '(MD) - Maryland',
    'md.': '(MD) - Maryland',
    'maryland': '(MD) - Maryland',

    'dc': '(DC) - District of Columbia',
    'd.c.': '(DC) - District of Columbia',

    # West
    'co': '(CO) - Colorado',
    'colo.': '(CO) - Colorado',

    'nv': '(NV) - Nevada',
    'nev.': '(NV) - Nevada',
    'nevada': '(NV) - Nevada',

    'ut': '(UT) - Utah',
    'utah': '(UT) - Utah',

    'wyoming': '(WY) - Wyoming',

    'id': '(ID) - Idaho',
    'idaho': '(ID) - Idaho',

    'mt': '(MT) - Montana',
    'mont.': '(MT) - Montana',

    'ak': '(AK) - Alaska',
    'alaska': '(AK) - Alaska',

    'hi': '(HI) - Hawaii',
    "hawai'i": '(HI) - Hawaii',
    'hawaii': '(HI) - Hawaii',
    'hi.': '(HI) - Hawaii',
}
# map for countries
international_map = {
    'ontario': 'Canada',
    'australia': 'Australia',
    'japan': 'Japan',
    'germany': 'Germany',
    'cameroon': 'Cameroon',
    'norway': 'Norway',
    'new zealand': 'New Zealand',
    'chile': 'Chile',
    'ghana': 'Ghana',
    'denmark': 'Denmark',
    'spain': 'Spain',
    'quebec': 'Canada',
    'nigeria': 'Nigeria',
    'london': 'England',
    'belgium': 'Belgium',
    'puerto rico': 'Puerto Rico',
    'novas': 'Canada',
    'portugal': 'Portugal',
    'purtugal': 'Portugal',
    'noord brabant': 'Netherlands',
    'catalonia': 'Spain',
    'netherlands': 'Netherlands',
    'france': 'France',
    'uk': 'United Kingdom',
    'rhineland-palatinate': 'Germany',
    'brasil': 'Brazil',
    'luxembourg': 'Luxembourg',
    'israel': 'Israel',
    'sweden': 'Sweden',
    'cyprus': 'Cyprus',
    'austria': 'Austria',
    'switzerland': 'Switzerland',
    'lesotho': 'Lesotho',
    'ireland': 'Ireland',
    'colombia': 'Colombia',
    'sierra leone': 'Sierra Leone',
    'canada': 'Canada',
    'italy': 'Italy',
    'village': 'Unknown',
    'mexico': 'Mexico',
    'congo': 'Congo',
    'tobago': 'Trinidad and Tobago',
    'kenya': 'Kenya',
    'jamaica': 'Jamaica',
    'togo': 'Togo',
    'uganda': 'Uganda',
    'hungary': 'Hungary',
    'serbia': 'Serbia',
    'north macedonia': 'North Macedonia',
    'iceland': 'Iceland',
    'ecuador': 'Ecuador',
    'venezuela': 'Venezuela',
    'czech republic': 'Czech Republic',
    'brazil': 'Brazil',
    'serbia': 'Serbia',
    'nepal': 'Nepal',
    'slovenia': 'Slovenia',
    'wales': 'Wales',
    'hong kong': 'Hong Kong',
    'ghana.': 'Ghana',
    'n.z.': 'New Zealand',
    'turks & caicos': 'Turks & Caicos',
    'trinidad & tobago': 'Trinidad and Tobago',
    'the netherlands': 'Netherlands',
    'morocco': 'Morocco',
    'republic of korea': 'South Korea',
    'grand cayman': 'Cayman Islands',
    'guatemala': 'Guatemala',
    'cayman islands': 'Cayman Islands',
    'turkey': 'Turkey',
    'saint lucia': 'Saint Lucia',
    'romania': 'Romania',
    'south africa': 'South Africa',
    'slovakia': 'Slovakia',
    'cape verde': 'Cape Verde',
    'egypt': 'Egypt',
    'ethiopia': 'Ethiopia',
    'malaysia': 'Malaysia',
    'china': 'China',
    'guam': 'Guam',
    'baja california': 'Mexico',
    'united kingdom': 'United Kingdom',
    'dominican republic': 'Dominican Republic',
    'senegal': 'Senegal',
    'ukraine': 'Ukraine',
    'panama': 'Panama',
    'argentina': 'Argentina',
    'costa rica': 'Costa Rica',
    'ivory coast': 'Ivory Coast',
    'mali': 'Mali',
    'barcelona': 'Spain',
    'gibraltar': 'Gibraltar',
    'latvia': 'Latvia',
    'india': 'India',
    'el salvador': 'El Salvador',
    'kosovo': 'Kosovo',
    'alberta': 'Canada',
    'poland': 'Poland',
    'democratic republic of congo': 'Democratic Republic of the Congo',
    'democratic republic of the congo': 'Democratic Republic of the Congo',
    'tanzania': 'Tanzania',
    'qc': 'Quebec',
    'gladbach': 'Germany',
    'nagano': 'Japan',
    'tokyo': 'Japan',
    'kanagawa': 'Japan',
    'russia': 'Russia',
    'united arab emirates': 'United Arab Emirates',
    'lithuania': 'Lithuania',
    'québec': 'Quebec',
    'reykjavik': 'Iceland',
    'gb-eng': 'England',
    'mozambique': 'Mozambique',
    'taiwan': 'Taiwan',
    'bavaria': 'Germany',
    'u.k.': 'United Kingdom',
    'noord-holland': 'Netherlands',
    'the netherlands': 'Netherlands',
    'republic of ireland': 'Ireland',
    'manchester': 'United Kingdom',
    'bl': 'Unknown',
    'haiti': 'Haiti',
    'slovenia': 'Slovenia',
    'bosnia and herzegovina': 'Bosnia and Herzegovina',
    'germany': 'Germany',
    'nova scotia': 'Canada',
    'nepal': 'Nepal',
    'czechia': 'Czech Republic',
    'valencia': 'Spain',
    'esp': 'Spain',
    'new south wales': 'Australia',
    'western australia': 'Australia',
    'fyn': 'Denmark',
    'ont.': 'Ontario',
    'ontario': 'Ontario',
    'british columbia': 'Canada',
    'b.c.': 'Canada',
    'quebec': 'Quebec',
    'novas': 'Canada'
}
# combine the maps
full_map = {**state_map, **international_map}
df['homeTown_state']=df['homeTown_state'].str.strip().str.lower().map(full_map)

# add international col for every player
def isInternational(player):
    states = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY',
    'DC']

    if pd.isna(player):
        return False
    elif '(' in player and ')' in player:
        abbrev = player[1: player.index(')')]
        return abbrev not in states
    else:
        return True
df['isInternational']=df['homeTown_state'].apply(isInternational) 


def height_filter(height_str):
    if pd.isna(height_str):
        return None

    try:
        height_str = str(height_str).strip()

        height_str = height_str.replace("′", "'").replace("''", "").replace('″', "").replace("’", "'").replace("‘", "'")
        height_str = height_str.replace(" ", "").replace("-", "'")

        if "'" in height_str:
            feet, inches = height_str.split("'")
            return int(feet) * 12 + int(inches)
        return None
    except:
        return None


def height_group(player):
    if pd.isna(player):
        return None
    elif player>=78:
        return '6\'6+'
    elif player>=72:
        return '6\'0-6\'6'
    elif player>=68:
        return '5\'8-5\'11'
    elif player>=63:
        return '5\'7-5\'3'
    else:
        return 'below 5\'3'
    
def weight_group(player): 
    try:
        if isinstance(player, str) and 'lbs' in player:
            player = player.lower().replace('lbs', '').strip()
        player = float(player)
    except:
        return None

    if pd.isna(player):
        return None
    elif player>=200:
        return 'Above 200'
    elif player>=170:
        return '170-199'
    elif player>=150:
        return '150-169'
    elif player>=130:
        return '130-149'
    else:
        return 'below 130'

df['weight_group']=df['weight'].apply(weight_group)
df['height_group']=df['height'].apply(height_filter).apply(height_group)

print(df)

# create a csv file
df.to_csv('d1_players_filtered.csv', index=False)






    