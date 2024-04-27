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

def create_post_json(conn, link):
    db_edit = conn.cursor()

    # get post writer, url and header
    post_title = db_edit.execute("SELECT title FROM posts WHERE link = ?", (link,)).fetchone()[0]
    post_author = db_edit.execute("SELECT name FROM authors WHERE author_id = ?", (db_edit.execute("SELECT author_id FROM posts WHERE link = ?", (link,)).fetchone()[0],)).fetchone()[0]

    return {'link': link, 'title': post_title, 'author': post_author}

print(create_post_json(conn, db_edit.execute("SELECT link FROM posts WHERE author_id = ?", (0,)).fetchone()[0]))

def send_json_to_server(server_address, json):
    r = requests.post(server_address, json=json)
    if r.status_code == 200:
        print("success")
        return r.status_code
    else:
        print("failed")
    
    

random_post_url = r"https://daff.co.il/p/44-%D7%9B%D7%9C%D7%91-%D7%94%D7%9C%D7%99%D7%99%D7%96%D7%A8-%D7%A2%D7%99%D7%93%D7%95-%D7%A9%D7%A8%D7%95%D7%9F"

def main():
    conn = create_connection('daff.db')
    json = create_post_json(conn, random_post_url)
    send_json_to_server("http://httpbin.org/post", json)


if __name__ == '__main__':
    main()