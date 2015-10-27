from pymongo import MongoClient
from bson.objectid import ObjectId

#establish access to the mongo database
client = MongoClient()
db = client.bloginator

#take in story id and return string of all lines for that story
def getStory(story_id):
	lines = db.lines.find({'story_id':ObjectId(story_id)})
	story = []
	for i in lines:
		story.append(i['data'])
	return story


def getTitle(story_id):
	return db.stories.find_one({'_id':ObjectId(story_id)})['title']


def getAllIds():
	raw_ids = db.stories.find()
	ids = []
	for i in raw_ids:
		ids.append(str(i['_id']))
	return ids


def newLine(story_id, user_id, line):
	db.lines.insert_one({
		'story_id':ObjectId(story_id),
		'user_id':ObjectId(story_id),
		'data':line
		})


def newStory(title):
	return str(db.stories.insert_one({
		'title':title
		}).inserted_id)

#if valid cred, return user_id
#else return -1
def auth(user, pw):
	result = db.users.find_one({'username':user, 'pw':pw})
	if result:
		return str(result['_id'])
	return -1

#Checks if user exists in the database
#If not, add them
def addUser(user, pw):
	result = db.users.find_one({'username':user})
	if result:
		return False # user already exists
	db.users.insert_one({
		'username':user,
		'pw':pw
		})
	return True