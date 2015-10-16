
import sqlite3
conn = sqlite3.connect("blog.db")
c = conn.cursor()
#takes in username and pw (plaintext for now) and returns boolean
#if credentials are valid


def getStory(story_id):

    c.execute('SELECT data FROM lines')
    lines = c.fetchall()
    return lines
    

#if valid cred, return user_id
#else return -1
def auth(user, pw):    
    q = "SELECT rowid FROM users where username = ? and pw = ? "
    c.execute(q, (user, pw) )
    result = c.fetchall()
    if len(result) == 1:
    	return result[0][0]
    return -1



