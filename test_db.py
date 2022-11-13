import os
import sqlite3
from sqlite3 import Error
import datetime
from split_txt_to_html import split_into_sentences

DATABASE = 'lecture_notes.db'

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def insert_lecture(cursor,lecture_title, lecture_author):
    lecture_sql = ''' INSERT INTO lectures(title, author)
              VALUES(?,?) '''
    lecture_task = (lecture_title,lecture_author)
    cursor.execute(lecture_sql, lecture_task)

def insert_sentence(cursor,lecture_id, sentence_id, sentence):
    sentence_sql = ''' INSERT INTO sentences(lecture_id, sentence_id,sentence)
              VALUES(?,?,?) '''
    sentence_task = (lecture_id, sentence_id, sentence)
    cursor.execute(sentence_sql, sentence_task)

def insert_comment(cursor, lecture_id, sentence_id, comment, user_id, date):
    comment_sql = ''' INSERT INTO comments(lecture_id, sentence_id,comment,user_id,date)
              VALUES(?,?,?,?,?) '''
    comment_task = (lecture_id, sentence_id, comment, user_id , date)
    cursor.execute(comment_sql, comment_task)

def get_lectures():
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT title, author FROM lectures")
    rows = cur.fetchall()
    return rows

def get_lecture_content(lecture_id, html = False):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT sentence_id, sentence FROM sentences WHERE lecture_id == ?", (lecture_id,))
    rows = cur.fetchall()
    cur.execute("SELECT title, author FROM lectures WHERE lecture_id == ?", (lecture_id,))
    lecture_title = cur.fetchall()
    if html == False:
        return rows
    else:
        html_content = f'<h2>{lecture_title[0][0]}</h2><br><h3>By {lecture_title[0][1]}</h3><p>'
        if len(rows) == 0:
            html_content += 'This lecture has no content'
        for row in rows:
            html_content += f'<a id = "s{row[0]}" class = "sentence"> {row[1]} </a><br>'
        html_content += "</p>"
        return html_content

def get_comments(lecture_id, sentence_id, html = False):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT comment,user_id,date FROM comments WHERE lecture_id = ? AND sentence_id = ? ", (lecture_id, sentence_id) )
    rows = cur.fetchall()
    if html == False:
        return rows
    else:
        sentence = ''
        if len(rows) == 0:
            sentence += 'No comments on this sentence'
        for row in rows:
            sentence += f'<div class = "comment"> On the {row[2]}, {row[1]} wrote: <br> {row[0]} </div><br>'
        return sentence

def init():
    database = r"lecture_notes.db"

    sql_create_lectures_table = """ CREATE TABLE IF NOT EXISTS lectures (
                                        lecture_id integer PRIMARY KEY,
                                        title text,
                                        author text
                                    ); """

    sql_create_sentences_table = """ CREATE TABLE IF NOT EXISTS sentences (
                                        id integer PRIMARY KEY,
                                        lecture_id integer NOT NULL,
                                        sentence_id integer NOT NULL,
                                        sentence text,
                                        FOREIGN KEY (lecture_id) REFERENCES lectures (lecture_id)
                                    ); """

    sql_create_comments_table = """CREATE TABLE IF NOT EXISTS comments (
                                    lecture_id integer,
                                    comment_id integer PRIMARY KEY,
                                    sentence_id integer NOT NULL,
                                    comment text NOT NULL,
                                    user_id integer NOT NULL,
                                    date datetime NOT NULL,
                                    FOREIGN KEY (sentence_id) REFERENCES sentences (sentence_id),
                                    FOREIGN KEY (lecture_id) REFERENCES sentences (lecture_id)
                                );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create lectures, sentences and comments table
        create_table(conn, sql_create_lectures_table)
        conn.commit()
        create_table(conn, sql_create_sentences_table)
        conn.commit()
        create_table(conn, sql_create_comments_table)
        conn.commit()
    else:
        print("Error! cannot create the database connection.")
    
    ### TEMPORARY INITIALISATION ###
    cur = conn.cursor()
    insert_lecture(cur,'Quantum', 'Aleks')
    rndm_sentences = list(('We made a big point in the previous chapter that quantum measurement is just some sort of quantum process.',' It represents an interaction between a quantum system and, well, us.',' A happy result of this interaction is that we get some information about the quantum state: a measurement outcome. ','Decoherence is what happens to a quantum state when some interaction with its environment causes the state the collapse, as if it had been measured. ','Unfortunately, it’s a particularly bad kind of measurement, because it happens sponta- neously and we don’t even get to know the outcome!'))
    for i, sentence in enumerate(rndm_sentences):
        insert_sentence(cur, 1,i, sentence)
    insert_lecture(cur,'What is an axolotl?', 'Mira')
    lecture_sentences = split_into_sentences('lecture_notes_demo.txt')
    for i, sentence in enumerate(lecture_sentences):
        insert_sentence(cur, 2,i, sentence)
    insert_comment(cur, 2, 2,'I don\'t believe that!', 1,datetime.datetime.now())
    insert_comment(cur, 2, 2,'I do', 2, datetime.datetime.now())
    insert_comment(cur, 2, 3,'This is true', 1, datetime.datetime.now())
    conn.commit()

def main():
    #init()
    print(get_lectures())
    print(get_comments(2,2))

if __name__ == '__main__':
    main()
