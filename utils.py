from os import urandom
from pymongo import MongoClient
from bson.objectid import ObjectId
from hashlib import sha512
from uuid import uuid4
from re import search

# a 32-byte key that should be used to secure the Flask session
secret_key = urandom(32);

#establish access to the mongo database
client = MongoClient()
db = client.bloginator

#take in story id and return all lines for that story, along with their ids
def getStoryLines(story_id):
	lines = db.lines.find({'story_id':ObjectId(story_id)})
	story = []
	for i in lines:
		story.append([i['data'], db.users.find_one({'_id':ObjectId(i['user_id'])})['username'], str(i['_id'])])
	return story


def getAllStories():
	raw_ids = db.stories.find()
	ids = []
	for i in raw_ids:
		ids.append([i['title'], db.users.find_one({'_id':ObjectId(i['user_id'])})['username'], str(i['_id'])])
	return ids


def newLine(story_id, user_id, line):
	return str(
		db.lines.insert_one({
			'story_id':ObjectId(story_id),
			'user_id':ObjectId(user_id),
			'data':line
			}).inserted_id
		)


def editLine(user_id, line_id, editedLine):
	result = db.lines.find_one({
		'user_id':ObjectId(user_id),
		'_id':ObjectId(line_id)
		})
	if result:
		db.lines.update(
			{'_id':ObjectId(line_id)},
			{'$set':{'data':editedLine}}
			)
		return True
	return False


def removeLine(user_id, line_id):
	result = db.lines.find_one({
		'user_id':ObjectId(user_id),
		'_id':ObjectId(line_id)
		})
	if result:
		db.lines.remove({
			'_id':ObjectId(line_id)
			})
		return True
	return False


def getLine(line_id):
	return db.lines.find_one({'_id':ObjectId(line_id)})['data']


def newStory(user_id, title):
	return str(
		db.stories.insert_one({
			'user_id':ObjectId(user_id),
			'title':title
			}).inserted_id
		)


def removeStory(user_id, story_id):
	result = db.stories.find_one({
		'user_id':ObjectId(user_id),
		'_id':ObjectId(story_id)
		})
	if result:
		db.stories.remove({
			'_id':ObjectId(story_id)
			})
		db.lines.remove({
			'story_id':ObjectId(story_id)
			})
		return True
	return False

#if valid cred, return user_id
#else return -1
def auth(user, pw):
	result = db.users.find_one({'username':user})
	if (
		result and
		sha512((pw + result['salt']) * 10000).hexdigest() == result['hash']
		):
		return str(result['_id'])
	return -1

#Checks if user exists in the database
#If not, add them
def addUser(user, pw):
	result = db.users.find_one({'username':user})
	if result:
		return False # user already exists
	salt = uuid4().hex
	db.users.insert_one({
		'username':user,
		'salt':salt,
		'hash':sha512((pw + salt) * 10000).hexdigest()
		})
	return True


def registrationError(user, pw, pw2):
	if pw != pw2:
		return 'Error: Passwords are not the same.'
	if len(user) < 1:
		return 'Error: Username must be at least 1 character long.'
	if len(pw) < 8:
		return 'Error: Password must be at least 8 characters long.'
	if not (
		bool(search('[0-9]', pw)) and
		bool(search('[a-zA-Z]', pw))
		):
		return 'Error: Password must contain both letters and digits.'
	return None
