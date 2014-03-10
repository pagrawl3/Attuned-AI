import pymongo
from pymongo import MongoClient
from roomDAO import *
from userDAO import *


class databaseUtility:

	rooms = None
	users = None
	db = None

	def __init__(self):
		print "::databaseUtility__init__"
		__all__ = ["getDatabase", "addUserToRoom", "removeUserFromRoom"
					,"addUserLikes", "getUserLikes","flushAll"]
		client = MongoClient()
		self.db = client['Attuned']
		self.rooms = roomDAO(self.db)
		self.users = userDAO(self.db)
		

	def getDatabase(self):
		client = MongoClient()
		#client = MongoClient('localhost', 27017)
		#db = client.test_database
		db = client['Attuned']
		return db

	def addUserToRoom(self,user, room):
		print "::addUserToRoom"
		if('usersInRoom' not in room):
			room['usersInRoom'] = list()
		userList = room['usersInRoom']
		#print userList
		userList.append(user)
		self.rooms.updateRoom(room)

	def removeUserFromRoom(self,user,room):
		print "::removeUserFromRoom"
		if('usersInRoom' not in room):
			return
		userList = room['usersInRoom']
		userList.remove(user)
		self.rooms.updateRoom(room)

	def addUserLikes(self,user,likes):
		print "::addUserLikes"
		if('likes' not in user):
			user['likes'] = None
		user['likes'] = likes
		self.users.updateUser(user)	


	def getUserLikes(self,user):
		#get all likes
		#get music likes
		#get non-music likes
		print "::getUserLikes"
		user = self.users.getUser(user)
		return user['likes']
	
	def flushAll(self):
		self.db.drop_collection("Rooms")
		self.db.drop_collection("Users")


# Main
# ============

db = databaseUtility()
rooms = db.rooms
users = db.users
db.flushAll()


room = {
			'name' :"Apt 34",
			'host' : "Pratham"
		}

shivam = {
			"facebook_id":"1234",
			"name":"Shivam"
		}

pratham = {
			"facebook_id":"4321",
			"name":"Pratham"
		}


rooms.addRoom(room['host'],room)
users.addUser(shivam['facebook_id'],shivam)
users.addUser(pratham['facebook_id'],pratham)

db.addUserToRoom(shivam,room)
db.addUserToRoom(pratham,room)

print rooms.getRoom()[0]

db.removeUserFromRoom(pratham,room)

print rooms.getRoom()[0]
