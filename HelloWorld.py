
from flask import Flask, request, render_template

app = Flask(__name__, static_url_path='')

@app.route('/')

def hello_person():
    return app.send_static_file('index.html')


