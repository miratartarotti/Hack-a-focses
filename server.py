#/* --- Imports --- */#
import os

from flask import Flask
from flask import render_template


app = Flask(__name__)

#/* --- Main --- */#
@app.route('/templates')
@app.route('/index.html')
def index(name=None): #Index page
    return render_template('index.html', name=name)

@app.route('/templates')
@app.route('/about.html')
def about(name=None): #About page
    return render_template('about.html', name=name)

@app.route('/templates')
@app.route('/test_db.html')
def about(name=None): #About page
    return render_template('test_db.html', name=name)


#/* start the server */#
if __name__ == '__main__':
    app.run()
