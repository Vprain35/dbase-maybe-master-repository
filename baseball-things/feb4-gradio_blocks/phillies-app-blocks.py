import sqlite3
import pandas as pd
import gradio as gr

#goal:
#make an app that will show a dropdown of every 1976 phillies player
#selecting a player (input) will display their number of home runs (output)
#do that but with gradio blocks

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


with gr.Blocks() as grIface:
    with gr.Row():
        with gr.Column():
            player_choice = gr.Dropdown(fetch_phillies(),interactive=True,value=None,label="Select a Player")
        with gr.Column():
            hrDisp = gr.Number(label="Number of Home runs:")

    player_choice.change(fn=f,inputs=[player_choice],outputs=[hrDisp])

grIface.launch()