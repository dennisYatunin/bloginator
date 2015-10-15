import sqlite3 as lite
import sys

con = None
try:
    con = lite.connect('blog.db')

    cur = con.connect()
def getStory()
{
    curs.con.cursor()
    cur.execute('SELECT data FROM lines')
    lines = cur.fetchall()
    return lines
    
}