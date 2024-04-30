import sqlite3
from sqlite3 import Error as SQLiteError
import requests
import pprint
from pathlib import Path 

def create_connection(db_file: str):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except SQLiteError as e:
        print(e)
    return conn

# Bonus 1:
# Write an api call to a fake server that sends a json file with the post and author details
def create_post_json(conn, post_id):
    db_edit = conn.cursor()

    # get post writer, url and header
    data = db_edit.execute('''
        SELECT posts.title, posts.link, a.n
        FROM posts, (
            SELECT authors.name n
            FROM authors
            where author_id = (
                SELECT posts.author_id
                FROM posts
                WHERE posts.post_id = 0
                )
            ) a
        WHERE post_id = 0
        ''').fetchone()
    return {'title': data[0], 'link': data[1], 'author': data[2]}

def send_json_to_server(server_address, json):
    r = requests.post(server_address, json=json)
    if r.status_code == 200:
        print("success")
        return r.status_code
    else:
        print("failed")

random_post_url = r"https://daff.co.il/p/44-%D7%9B%D7%9C%D7%91-%D7%94%D7%9C%D7%99%D7%99%D7%96%D7%A8-%D7%A2%D7%99%D7%93%D7%95-%D7%A9%D7%A8%D7%95%D7%9F"

# Bonus 2:
# Write an SQL query that extracts all posts joined with their authors from the DB
def posts_joined_by_authors(conn):
    db_edit = conn.cursor()
    return db_edit.execute('''
        SELECT Authors.name, Posts.link, Posts.title
        FROM Authors
        INNER JOIN Posts
        ON Authors.author_id = Posts.author_id
        ''').fetchall()

# Bonus 3:
# Write an SQL query that extracts the most recent post for each author
def most_recent_post_for_each_author(conn):
    db_edit = conn.cursor()
    return db_edit.execute('''
        SELECT posts.link, authors.name
        FROM posts
        LEFT JOIN authors
        ON authors.author_id = posts.author_id
        GROUP BY posts.author_id
        ''').fetchall()

def main():
    conn = create_connection('daff.db')
    json = create_post_json(conn, 0)
    print(json)
    send_json_to_server("http://httpbin.org/post", json)

    print("#############\n\nBonus2:\n\n#############")
    pprint.pprint(posts_joined_by_authors(conn))
    
    print("#############\n\nBonus3:\n\n#############")
    pprint.pprint(most_recent_post_for_each_author(conn))



if __name__ == '__main__':
    main()