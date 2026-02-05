import sqlite3
import pandas as pd

#data context: 
#batting table:
#each record is a player in a specific season (multiple seasons = multiple entries)
#any trades mid-year will also be an other entry, including being traded back to the same team
#unique entries: a player, in a specific season, with a specific team, for an uninterrupted period of time (each stint?)


conn = sqlite3.connect('../baseball.db')
cursor = conn.cursor()
query = '''
    SELECT playerID,count(*)
    FROM batting 
    WHERE yearID = 1976
    GROUP BY playerID
    HAVING count(*) = 2
    ORDER BY count(*) DESC;
'''
cursor.execute(query)
records = cursor.fetchall()
conn.close()

#changing which results you want will require chanign the dataframe columns
recordsDF = pd.DataFrame(records)#,columns=['teamID','yearlyHR'])
print(recordsDF)


#pull specific colunms w/ SELECT ___ FROM table
#pull specific rows w/ WHERE ___
#chaining WHERE conditions: WHERE HR > 20 AND yearID = 1967 OR yearID = 1976