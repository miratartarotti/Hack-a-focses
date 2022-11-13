#/* --- Imports --- */#
import os
import datetime

from flask import Flask, Markup, request, abort
from flask import render_template

import test_db


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

@app.route("/api/notes/<lecture_id>/comments/s<sentence>")
def load_comments(lecture_id, sentence):
    return test_db.get_comments(lecture_id, sentence, html = True)

@app.route("/api/notes/<lecture_id>/comments/s<sentence>/add", methods=["POST"])
def add_comment(lecture_id, sentence):
    author = request.form["author"]
    comment = request.form["comment"]
    date = datetime.datetime.now()

    print(f"Attempting to add comment by {author} on {date}:\n\t\"{comment}\"")

    conn = test_db.create_connection(test_db.DATABASE)
    if conn is None:
        return abort(500)

    cur = conn.cursor()
    try:
        test_db.insert_comment(cur, lecture_id, sentence, comment, author, date)
    except Exception as e:
        print(e)
        return abort(500)
    finally:
        conn.commit()
    return "OK"

@app.route("/l<lecture_id>")
def load_lecture(lecture_id):
    contents = test_db.get_lecture_content(lecture_id, html = True)
    return render_template("lecture_notes.html",
                           lecture_id = lecture_id,
                           lecture_contents = Markup(contents))

#/* start the server */#
if __name__ == '__main__':
    app.run()
