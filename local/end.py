from flask import Flask, render_template
from flask import templating
import os
import webbrowser 
import thread

app = Flask("DSP")
links = ['ss']

def open_site():
    return webbrowser.open_new("http://127.0.0.1:5000/")

def create_site(l):
    global links
    links = l
    open_site()
    thread.start_new_thread(app.run(debug=False), debug=False)
    return os.system("start \"\" http://127.0.0.1:5000/ ")




@app.route('/')
def idx(): 
    return render_template('index.html', links=links)


if __name__ == '__main__':
    create_site(['/Users/steinn/dsp/dsp_Assignment_1/ToHTML/202-1-5391.html'])