import gradio as gr

def square(x):
    return x**2

def add(x,y):
    return x+y

with gr.Blocks() as iface:
    with gr.Row():
        app_input = gr.Number(label = "Type in a number:")
        app_output = gr.Number(label = "This is the square of the number:")
        app_input.change(fn=square,inputs=[app_input],outputs=[app_output])

    with gr.Row():
        gr.Label("test divide")


    with gr.Row():
        with gr.Column():
            xBox = gr.Number(label="Type a number:")
            yBox = gr.Number(label="Type another number:")
        with gr.Column():
            addition_output = gr.Number(label="sum of the two numbers:")

    xBox.change(fn=add, inputs=[xBox,yBox],outputs=[addition_output])
    yBox.change(fn=add, inputs=[xBox,yBox],outputs=[addition_output])

    #xbox and ybox on the same row
    with gr.Row():
        with gr.Column():
            xBox2 = gr.Number(label="Type a number:")
            addition_output2 = gr.Number(label="sum of the two numbers:")
        with gr.Column():
            yBox2 = gr.Number(label="Type another number:")

    xBox2.change(fn=add, inputs=[xBox2,yBox2],outputs=[addition_output2])
    yBox2.change(fn=add, inputs=[xBox2,yBox2],outputs=[addition_output2])
    

iface.launch()