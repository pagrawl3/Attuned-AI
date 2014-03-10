from pprint import pprint
import pymongo


class roomDAO:

	rooms = None
	
	def __init__(self,database):
		print "::roomDAO__init__"
		__all__ = ["addRoom", "deleteRoom", "getRoom","updateRoom"]
		self.data = []
		db = database;
		self.rooms = db['Rooms']

	def addRoom(self,host,room=None):
		print "::addRoom"
		if (room!=None):
			room['host']=host
			room_id = self.rooms.insert(room)
			return room_id

		room = {'host':host}
		room_id = self.rooms.insert(room)
		return room_id
	
	def deleteRoom(self,roomID = None, host = None):
		print "::deleteRoom"
		if(roomID!=None):
			self.rooms.remove({"_id": roomID})
		if(host!=None):
			self.rooms.remove({"host":host})

	def getRoom(self,roomID = None, host = None):
		print "::getRoom"
		if(roomID!=None):
			return self.rooms.find_one({"_id":roomID})
		if(host!=None):
			return self.rooms.find_one({"host":host})
		return self.rooms.find()		

	def updateRoom(self,roomInfo, roomID = None, host = None,returnValue=False):
		print "::updateRoom"
		if(roomID!=None):
			roomInfo["_id"]=roomID
		else:roomID=roomInfo["_id"]
		
		if(host!=None):
			roomInfo["host"]=host
		else:host=roomInfo["host"]

		room = self.getRoom(roomID,host)
		self.rooms.update(room,roomInfo)#,{ upsert: true }
		if(returnValue==True):
			return self.getRoom(roomID=roomID)