class userDAO:

	users = None

	
	def __init__(self,database):
		print "::userDAO__init__"
		__all__ = ["addUser", "deleteUser", "getUser","updateUser"]
		self.data = []
		db = database;
		self.users = db['Users']

	def addUser(self,facebook_id,user = None):
		print "::addUser"
		if (user!=None):
			user['facebook_id']=facebook_id
			user_id = self.users.insert(user)
			return user_id

		user = {'facebook_id' : facebook_id}
		user_id = self.users.insert(user)
		return user_id	

	def deleteUser(self,userID = None, facebook_id = None):
		print "::deleteUser"
		if(userID!=None):
			self.users.remove({"_id": userID})
		if(facebook_id!=None):
			self.users.remove({"facebook_id": facebook_id})

	def getUser(self,userID = None, facebook_id = None):
		print "::getUser"
		#print facebook_id
		if(userID != None):
			return self.users.find_one({"_id":userID})
		if(facebook_id != None):
			return self.users.find_one({"facebook_id":facebook_id})
		return self.users.find()

	def updateUser(self,userInfo, userID = None, facebook_id = None, returnValue=False):
		print "::updateUser"
		if(userID!=None):
			userInfo["_id"] = userID
		else: userID = userInfo["_id"]

		if(facebook_id!=None):
			userInfo["facebook_id"]=facebook_id
		else: facebook_id = userInfo["facebook_id"]

		user = self.getUser(userID,facebook_id)
		self.users.update(user,userInfo) #,{ upsert: true }
		if(returnValue==True):
			return self.getUser(facebook_id=facebook_id)