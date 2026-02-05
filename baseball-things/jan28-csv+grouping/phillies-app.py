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
        SELECT playerID,HR
        FROM batting
        WHERE teamID = 'PHI' AND yearID = 1976;
    '''
    cursor.execute(query)
    records = cursor.fetchall()
    conn.close()

    #class work below
    #playerss = []
    #for record in records:
    #    players.append(record[0])
    #return players

    #look im kinda off in my own world here,
    global playersLi
    global HRsLi
    playersLi = []
    HRsLi = []
    for record in records:
        playersLi.append(record[0])
        HRsLi.append(record[1])
    return playersLi


def f(player):
    for i in range(len(playersLi)):
        if playersLi[i] == player:
            HR = int(HRsLi[i])
            break
    return HR

#print(f('allendi01'))

#class work immediately below
#grIface = gr.Interface(fn = f,inputs = gr.Dropdown(fetch_phillies()),outputs = "number")


#more of me being in my own world
grIface = gr.Interface(fn = f,inputs = gr.Dropdown(fetch_phillies(),value=None),outputs = "number", live = True)

grIface.launch()