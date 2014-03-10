import pylast
import json
import pymongo
import pyechonest
from pprint import pprint

from pyechonest import artist
from pymongo import MongoClient

import Database
from Database.databaseUtility import databaseUtility
from Database.userDAO import userDAO
from Database.roomDAO import roomDAO

from lastfm import lastfm

'''
import Database
from Database import databaseUtility
from Database import roomDAO
from Database import userDAO
'''
import json
from pprint import pprint

dataset = {
	
		'apt34' : {
					'name' :"Apt 34",
					'host' : "Pratham"
				},

		'Shivam' : {
					"facebook_id":"1234",
					"name":"Shivam"
				},

		'Pratham' : {
					"facebook_id":"4321",
					"name":"Pratham"
				}


		}

def read(name):
	json_data=open(name+'.json')
	data = json.load(json_data)
	#print data[5]
	#pprint(data)
	json_data.close()
	return data

#dataset['Likes'] = read()

#create user,rooms
db = databaseUtility()
rooms = db.rooms
users = db.users
db.flushAll()
rooms.addRoom(dataset['apt34']['host'],dataset['apt34'])
users.addUser(dataset['Shivam']['facebook_id'],dataset['Shivam'])
users.addUser(dataset['Pratham']['facebook_id'],dataset['Pratham'])

#get user likes
shivam = dataset['Shivam']
shivam.update(read(shivam['name']))
shivam = users.updateUser(shivam, returnValue = True)

pratham = dataset['Pratham']
pratham.update(read(pratham['name']))
pratham = users.updateUser(pratham, returnValue = True)

#add user to rooms
apt34 = dataset['apt34']
db.addUserToRoom(shivam,apt34)
db.addUserToRoom(pratham,apt34)
'''
#pprint(pratham['music'])
#print pratham['music']
prat = users.getUser(facebook_id=pratham['facebook_id'])
#print prat['music']
#for user in users.getUser():
#pprint(users.getUser(facebook_id=shivam['facebook_id']))
	#print user
'''
#get favourite artist : or/music/tracks/genres/albums

artists = list()
users = rooms.getRoom(host = apt34['host'])['usersInRoom']
for user in  users:
	for item in user['music']:
		if(item['category']=="Musician/band"):
			artists.append(item)
l = lastfm()
#print "Liked Artists : ",len(artists)
likedArtist = len(artists)
ratio =.6
artistCount = int((120/likedArtist)*ratio)
trackCount = int((120/likedArtist)*(1-ratio))
total = likedArtist*artistCount*trackCount
print "(likedArtist,artistCount,trackCount)(%s, %s, %s)"%(likedArtist,artistCount,trackCount)
print "total : ",total
weight_currentness = .5
weight_similarness = .8
reco = 	l.getRecommendation(artists,artistCount,trackCount,weight_currentness, weight_similarness)		
#pprint(reco)
l.displayList(reco)
#pprint(artists)			
	#if(len(user['music'])==0):continue

	

#get similar-popular tracks
#return list
