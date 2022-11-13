#/* --- Imports --- */#
import os
import test_db

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
def about_page(name=None): #About page
    return render_template('about.html', name=name)

@app.route('/templates')
@app.route('/test_db.html')
def about(name=None): #About page
    return render_template('test_db.html', name=name)

@app.route("/api/notes/<lecture_notes>/comments/s<sentence>")
def load_comments(lecture_notes, sentence):
    return test_db.get_comments(lecture_notes, sentence, html = True)

@app.route("/lecture/<lecture_id>")
def load_lecture(lecture_id):
    contents = test_db.get_lecture_content(lecture_id, html = True)
    return render_template("/templates/lecture_notes.html",
                           lecture_id = lecture_id,
                           lecture_contents = contents)

#/* start the server */#
if __name__ == '__main__':
    app.run()
