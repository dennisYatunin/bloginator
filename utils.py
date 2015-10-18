
import sqlite3

conn = sqlite3.connect("blog.db", check_same_thread=False)
c = conn.cursor()

#takes in username and pw (plaintext for now) and returns boolean
#if credentials are valid



#takes in username and pw (plaintext for now) and returns userid or -1 if invalid
#if credentials are valid

def getStory(story_id):

	c.execute('SELECT data FROM lines WHERE story_id = ?;', (str(story_id)))
	lines = c.fetchall()[0]
	print lines
	story = ""
	for i in lines:
		print i
		story += i[0] + " \n"
		conn.commit()
	return  story
	conn.commit()




#if valid cred, return user_id
#else return -1
def auth(user, pw):

    q = "SELECT rowid FROM users where username = ? and pw = ?;"
    c.execute(q, (user, pw) )
    result = c.fetchall()
    if len(result) == 1:
    	return result[0][0]
	conn.commit()
    return -1

def addUser(user, pw):
    c.execute("INSERT INTO users VALUES (?, ?);", (user, pw))
    conn.commit()

