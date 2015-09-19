
from flask import Flask
import random
from flask import render_template

app = Flask(__name__)
app.secret_key = 'This is really unique and secret'

@app.route('/')

def hello_person():
    return render_template('Test.html')


if __name__ == '__main__':
    app.run()
