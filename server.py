#/* --- Imports --- */#
import os
import test_db

from flask import Flask, Markup
from flask import render_template


app = Flask(__name__)

#/* --- Main --- */#
@app.route("/index.html")
@app.route("/")
def load_lecture_list():
    contents = test_db.get_lectures(html=True)
    print(contents)
    return render_template("index.html",lecture_list = Markup(contents))

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

@app.route("/l<lecture_id>")
def load_lecture(lecture_id):
    contents = test_db.get_lecture_content(lecture_id, html = True)
    return render_template("lecture_notes.html",
                           lecture_id = lecture_id,
                           lecture_contents = Markup(contents))

#/* start the server */#
if __name__ == '__main__':
    app.run()
