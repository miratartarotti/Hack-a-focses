#/* --- Imports --- */#
import os
import test_db

from flask import Flask
from flask import render_template


app = Flask(__name__)

#/* --- Main --- */#
@app.route('/')
def index(name=None): #Index page
    return render_template('index.html', name=name)

@app.route('/templates')
@app.route('/about.html')
def about_page(name=None): #About page
    return render_template('about.html', name=name)

@app.route('/admin')
def admin():
    return "Nice try."

@app.route('/templates')
@app.route('/test_db.html')
def about(name=None): #About page
    return render_template('test_db.html', name=name)

@app.route("/api/notes/<lecture_notes>/comments/s<sentence>")
def load_comments(lecture_notes, sentence):
    return test_db.get_comments(lecture_notes, sentence, html = True)
    return """
    <div class="comment">
    Good idea!!
    </div>

    <div class="comment">
    Meh :(
    </div>
    """

#/* start the server */#
if __name__ == '__main__':
    app.run()
