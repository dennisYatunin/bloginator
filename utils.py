
import sqlite3



#take in story id and return string of all lines for that story
def getStory(story_id):
	conn = sqlite3.connect("blog.db", check_same_thread=False)
	c = conn.cursor()
	c.execute('SELECT data FROM lines WHERE story_id = ?;', (str(story_id)))
	lines = c.fetchall()
	#print lines
	story = []
	for i in lines:
		#print i
		story += [ i[0] ]
	conn.close()
	return  story
#testing - DONE
# print "testing getStory"
# print getStory(1) #returns all the lines
# print getStory(2) #return nothing :)

def getTitle(story_id):
	conn = sqlite3.connect("blog.db", check_same_thread=False)
	c = conn.cursor()
	q = "SELECT title FROM stories WHERE rowid = ? ;"
	c.execute(q, (story_id,))
	title = c.fetchall()[0][0]
	return title
#TESTING -done
print getTitle(1)

def getAllIds():
	conn = sqlite3.connect("blog.db", check_same_thread=False)
	c = conn.cursor()
	q = "SELECT rowid FROM stories;"
	c.execute(q)
	raw_ids = c.fetchall()
	ids = []
	for i in raw_ids:
		ids += [ i[0] ]
	return ids
# #TESTING - DONE
# print getAllIds()

def newLine(story_id, user_id, line):
    conn = sqlite3.connect("blog.db", check_same_thread=False)
    c = conn.cursor()
    q = "INSERT INTO lines VALUES (?, ?, ?);"
    c.execute(q, (story_id, user_id, line))
    conn.commit()
    conn.close()
#TESTING - done
# print newLine(1,6,"newline added thru function")
# print getStory(1)

def newStory(title):
	conn = sqlite3.connect("blog.db", check_same_thread=False)
	c = conn.cursor()
	q = "INSERT INTO stories VALUES ( ? );"
	c.execute(q, (title,) )
	q = "SELECT rowid FROM stories WHERE title = ? ;"
	c.execute(q, (title,) )
	result = c.fetchall()
	conn.commit()
	conn.close()
	return result[0][0]
# TESTING
# x = newStory("once upon a time.")
# print x
# print newLine(x, 1, "newline for new story")
# print getStory(x)

#if valid cred, return user_id
#else return -1
def auth(user, pw):
	conn = sqlite3.connect("blog.db", check_same_thread=False)
	c = conn.cursor()
	q = "SELECT rowid FROM users where username = ? and pw = ?;"
	c.execute(q, (user, pw) )
	result = c.fetchall()
	if len(result) == 1:
		return result[0][0]
	conn.close()
	return -1
# TESTING- DONE
# print "testing auth"
# print auth("loren", "loren") #returns id 1
# print auth("yo", "no") #returns -1



#Checks if user exists in the database
#If not, add them
def addUser(user, pw):
	conn = sqlite3.connect("blog.db", check_same_thread=False)
	c = conn.cursor()
	c.execute("SELECT rowid FROM users where username = ? ;", (user,))
	result = c.fetchall()
	if len(result) > 0:
		return False # user already exists
	c.execute("INSERT INTO users VALUES (?, ?);", (user, pw))
	conn.commit()
	conn.close()
	return True
# #Testing - DONE
# print addUser("test", "test")
# print auth("test", "test")
