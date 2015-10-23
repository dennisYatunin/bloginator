import sqlite3

conn = sqlite3.connect("blog.db", check_same_thread=False)
c = conn.cursor()

#take in story id and return string of all lines for that story
def getStory(story_id):
	c.execute('SELECT data FROM lines WHERE story_id = ?;', (str(story_id)))
	lines = c.fetchall()
	#print lines
	story = []
	for i in lines:
		#print i
		story += [ i[0] ]
	return  story


def getTitle(story_id):
	q = "SELECT title FROM stories WHERE rowid = ? ;"
	c.execute(q, (story_id,))
	title = c.fetchall()[0][0]
	return title


def getAllIds():
	q = "SELECT rowid FROM stories;"
	c.execute(q)
	raw_ids = c.fetchall()
	ids = []
	for i in raw_ids:
		ids += [ i[0] ]
	return ids


def newLine(story_id, user_id, line):
        q = "INSERT INTO lines VALUES (?, ?, ?);"
        c.execute(q, (story_id, user_id, line))
        conn.commit()



def newStory(title):
        q = "INSERT INTO stories VALUES ( ? );"
        c.execute(q, (title,) )
        q = "SELECT rowid FROM stories WHERE title = ? ;"
        c.execute(q, (title,) )
        result = c.fetchall()
        conn.commit()
        return result[0][0]

#if valid cred, return user_id
#else return -1
def auth(user, pw):
	q = "SELECT rowid FROM users where username = ? and pw = ?;"
	c.execute(q, (user, pw) )
	result = c.fetchall()
	if len(result) == 1:
		return result[0][0]

	return -1

#Checks if user exists in the database
#If not, add them
def addUser(user, pw):
	c.execute("SELECT rowid FROM users where username = ? ;", (user,))
	result = c.fetchall()
	if len(result) > 0:
		return False # user already exists
	c.execute("INSERT INTO users VALUES (?, ?);", (user, pw))
	conn.commit()
	return True

