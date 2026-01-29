import sqlite3
import pandas as pd

#data context: 
#each record is a player in a specific season (multiple seasons = multiple entries)
#any trades mid-year will also be an other entry, including being traded back to the same team
#unique entries: a player, in a specific season, with a specific team, for an uninterrupted period of time (each stint?)


conn = sqlite3.connect('baseball.db')
#cursor = conn.cursor
dfData = pd.read_csv('teams.csv')
dfData.to_sql('teams',conn, if_exists='replace', index=False)
conn.commit()
conn.close()