import pymongo
from pymongo import MongoClient
from roomDAO import *
from userDAO import *

def getDatabase():
	client = MongoClient()
	#client = MongoClient('localhost', 27017)
	#db = client.test_database
	db = client['Attuned']
	return db
'''
def addUserToRoom():
	#do something
def removeUserFromRoom():
	#do something
def getUserLikes():
	#get all likes
	#get music likes
	#get non-music likes

'''
db = getDatabase()
db.drop_collection("Rooms")
db.drop_collection("Users")
rooms = roomDAO(db)
users = userDAO(db)

#print db.collection_names()#list all collections

rooms.addRoom("Shivam")
'''
for room in rooms.getRoom():
	print room
'''
users.addUser("1234",{"name":"Kid"})

'''
for user in users.getUser():
	print user
'''
user =  users.getUser(facebook_id="1234")
user["pet"]="dog"

#print users.update(user,returnValue=True)
#users.update(user,returnValue=True)


#posts.find_one({"author": "Mike"})
#posts.find_one({"_id": post_id})