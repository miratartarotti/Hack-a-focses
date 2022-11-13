#/* --- Imports --- */#
import os
import datetime

from flask import Flask, Markup, request, abort, redirect
from flask import render_template
from werkzeug.utils import secure_filename
import test_db
from split_txt_to_html import split_into_sentences


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

@app.route('/admin') #Prevent curiosity
def admin():
    return "Nice try."

@app.route('/templates')
@app.route('/test_db.html')
def about(name=None): #Load TestDB
    return render_template('test_db.html', name=name)

@app.route("/api/notes/<lecture_notes>/comments/s<sentence>")
def load_comments(lecture_notes, sentence): #Load lecture comments from DB
    return test_db.get_comments(lecture_notes, sentence, html = True)

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
def load_lecture(lecture_id): #Get lecture from DB
    contents = test_db.get_lecture_content(lecture_id, html = True)
    return render_template("lecture_notes.html",
                           lecture_id = lecture_id,
                           lecture_contents = Markup(contents))

@app.route('/upload', methods = ['POST', 'GET'])
def upload():
    print('upload')
    if request.method == 'POST':
        f = request.files['file']
        filename = secure_filename(f.filename)
        f.save('static/uploads/' + filename)
        lecture_sentences = split_into_sentences('static/uploads/'+filename)
        conn = test_db.create_connection(test_db.DATABASE)
        cur = conn.cursor()
        for i, sentence in enumerate(lecture_sentences):
            if i == 0:
                title = sentence
                continue
            if i == 1:
                author = sentence
                test_db.insert_lecture(cur,title, author)
                cur.execute("SELECT MAX(lecture_id) FROM lectures")
                lecture_number = cur.fetchall()[0][0]

                continue
            print(lecture_number,i-1, sentence)
            test_db.insert_sentence(cur, lecture_number,i-1, sentence)
        conn.commit()
        
        #process the file in the database
        return redirect("/")

#/* start the server */#
if __name__ == '__main__':
    app.run()
