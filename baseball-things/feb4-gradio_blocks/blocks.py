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
            first_addor = gr.Number(label="Type a number:")
            second_addor = gr.Number(label="Type another number:")
        with gr.Column():
            addition_output = gr.Number(label="sum of the two numbers:")

    first_addor.change(fn=add, inputs=[first_addor,second_addor],outputs=[addition_output])
    second_addor.change(fn=add, inputs=[first_addor,second_addor],outputs=[addition_output])
    

iface.launch()