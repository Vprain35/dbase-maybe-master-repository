import gradio as gr
import pandas as pd
import sqlite3

#dropdown w top 10 phillies hr hitters of all time (first and last name) (in alphabetical order by last name), when selected, displays a graph of thier HRs over time (by year)

def get_top_hitters():
    conn = sqlite3.connect('../baseball.db')
    cursor = conn.cursor()
    query = '''
        WITH top_hitters AS (
        SELECT people.nameFirst,people.nameLast,batting.playerID FROM people INNER JOIN batting ON people.playerID=batting.playerID 
        WHERE batting.teamID = 'PHI'
        GROUP BY batting.playerID
        ORDER BY SUM(batting.HR) DESC LIMIT 10)

        SELECT CONCAT(nameFirst,' ',nameLast),playerID
        FROM top_hitters
        ORDER BY nameLast
    '''
    
    #dropdown displays the first of every entry, and returns the second as the output

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return results

def get_hr_data(playerID):
    conn = sqlite3.connect('../baseball.db')
    cursor = conn.cursor()
    query = '''
        SELECT CAST(yearID AS text),SUM(HR) FROM batting
        WHERE playerID = ? AND teamID='PHI'
        GROUP BY yearID
        ORDER BY yearID ASC
    '''

    cursor.execute(query,[playerID])
    results = cursor.fetchall()
    conn.close()

    df = pd.DataFrame(results,columns=["year","home runs"])
    return(df)


with gr.Blocks() as grIface:
    with gr.Row():
        #dropdown displays the first of every entry, and returns the second as the output
        player_choice = gr.Dropdown(get_top_hitters(),interactive=True,value=None,label="Select a Player")
    with gr.Row():
        #bc it will always be given an input, we dont have to define a func to act as one
        hr_graph = gr.LinePlot(value=None,x="year",y="home runs")

    player_choice.change(fn = get_hr_data, inputs=[player_choice],outputs=[hr_graph])


grIface.launch()