
import sqlite3

#takes in username and pw (plaintext for now) and returns userid or -1 if invalid
#if credentials are valid

def getStory(story_id):
    conn = sqlite3.connect("blog.db")
    c = conn.cursor()
    c.execute('SELECT data FROM lines WHERE story_id = ?', (str(story_id)))
    lines = c.fetchall()[0]
    print lines
    story = ""
    for i in lines:
        print i
        story += i[0] + " \n"

    return story    

#if valid cred, return user_id
#else return -1
def auth(user, pw):
    conn = sqlite3.connect("blog.db")
    c = conn.cursor()
    q = "SELECT rowid FROM users where username = ? and pw = ? "
    c.execute(q, (user, pw) )
    result = c.fetchall()
    if len(result) == 1:
        return result[0][0]
    return -1

def addUser(user, pw):
    conn = sqlite3.connect("blog.db")
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?, ?)", (user, pw))
    


