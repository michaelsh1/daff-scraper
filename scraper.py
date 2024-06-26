from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
import sqlite3
from sqlite3 import Error
import regex as re

URL = 'https://daff.co.il/'

def create_connection(db_file: str):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def how_many_pages(html):
    return 10
    # another return in case you want to scrape the entire site.
    # return int(re.search(">(\d+)</a></span> <span class=\"page next", html).group(1))

def create_tables(conn):
    db_edit = conn.cursor()

    # create table
    db_edit.execute('''CREATE TABLE IF NOT EXISTS 
                    posts(link, title, author_id, post_id)''')
    db_edit.execute('''CREATE TABLE IF NOT EXISTS
                    authors(name, author_id)''')

    conn.commit()

def daff_scrape(conn, FIRST_PAGE=1):
    # the author id if you add a new author
    author_id = 0
    post_id = 0

    # open first url (for counting pages)
    try: ### change 1: code fails if no internet connection
        html = urlopen(URL).read().decode('utf-8')
    except:
        print("failed to open url")
        return

    for page in range(FIRST_PAGE, how_many_pages(html) + 1):
        print("###### page: " + str(page) + " ######") # cli
        
        # open current url
        page_url = URL + '?page=' + str(page)
        html = urlopen(page_url).read().decode('utf-8')

        # get all posts
        soup = bs(html, features="html.parser")
        posts_list = soup.find_all("div", class_="single_post")

        # iterate over posts
        for post in posts_list:
            post_id, author_id = insert_post(conn, post, post_id, author_id)

        conn.commit()

def insert_post(conn, post, post_id, author_id=0):
    db_edit = conn.cursor()
    # get post writer, url and header
    post_writer = post.find("a", class_="post_writer").text
    post_url = URL + post.find("a", class_=None).get('href')
    post_header = post.find("a", class_=None).text
    active_post_id = author_id

    # check if post is already in table
    if (db_edit.execute("SELECT link FROM posts WHERE link = ?", (post_url,)).fetchall() != []):
        print("post (and author) already in table") # cli
        return post_id, author_id
    # check if author is already in table
    if (db_edit.execute("SELECT author_id FROM authors WHERE name = ?", (post_writer,)).fetchall() == []):
        # if not, add to table
        db_edit.execute("INSERT OR IGNORE INTO authors VALUES (?, ?)", (post_writer, author_id))
        print("added author: " + post_writer + ", id: " + str(author_id)) # cli
        author_id += 1
    else:
        # if yes, get id
        active_post_id = db_edit.execute("SELECT author_id FROM authors WHERE name = ?", (post_writer,)).fetchone()[0]
    # and add to posts table
    db_edit.execute("INSERT OR IGNORE INTO posts VALUES (?, ?, ?, ?)", (post_url, post_header, active_post_id, post_id))
    print("added post: " + post_header + ", id: " + str(post_id)) # cli
    post_id += 1

    return post_id, author_id


def main():
    # connect to db
    conn = create_connection('daff.db')

    # create tables
    create_tables(conn)

    daff_scrape(conn)
    
if __name__ == '__main__':
    main()