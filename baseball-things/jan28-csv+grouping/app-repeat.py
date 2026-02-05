import sqlite3
import pandas as pd
import gradio as gr

#goal:
#make an app that will show a dropdown of every 1976 phillies player
#selecting a player (input) will display their number of home runs (output)

def fetch_phillies():
    conn = sqlite3.connect('../baseball.db')
    cursor = conn.cursor()
    query = '''
        SELECT playerID
        FROM batting
        WHERE teamID = 'PHI' AND yearID = 1976;
    '''
    cursor.execute(query)
    records = cursor.fetchall()
    conn.close()

    #class work below
    players = []
    for record in records:
        players.append(record[0])
    return players


def f(player):
    conn = sqlite3.connect('../baseball.db')
    cursor = conn.cursor()
    query = '''
        SELECT HR
        FROM batting
        WHERE teamID = 'PHI' AND yearID = 1976 AND playerID = ?;
    '''
    
    cursor.execute(query,[player])
    records = cursor.fetchall()
    conn.close()

    return records


grIface = gr.Interface(fn = f,inputs = gr.Dropdown(fetch_phillies()),outputs = "number", live = True)


grIface.launch()