import sqlite3
from sqlite3 import Error
import requests
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

conn = create_connection('daff.db')
db_edit = conn.cursor()

print(db_edit.execute("SELECT name FROM authors WHERE author_id = ?", (10,)).fetchone()[0])

# def create_post_json(conn, link):
#     db_edit = conn.cursor()

#     # get post writer, url and header
#     post_title = db_edit.execute("SELECT title FROM posts WHERE link = ?", (link,)).fetchone()[0]
#     post_author = db_edit.execute("SELECT name FROM authors WHERE author_id = ?", (db_edit.execute("SELECT author_id FROM posts WHERE link = ?", (link,)).fetchone()[0],)).fetchone()[0]

#     return {'link': link, 'title': post_title, 'author': post_author}

# print(create_post_json(conn, db_edit.execute("SELECT link FROM posts WHERE author_id = ?", (0,)).fetchone()[0]))

# def send_json_to_server(server_address, json):
#     r = requests.post(server_address, json=json)
#     if r.status_code == 200:
#         print("success")
#     else:
#         print("failed")
    
    