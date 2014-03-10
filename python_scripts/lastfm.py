import pylast
import json
import pyechonest
from pyechonest import artist
from pprint import pprint

class lastfm:

	network = None


	def __init__(self):
		print "::lastfm__init__"
		__all__ = ["getSimilarArtists", "getSimilarTracks", "getAllTopTracks"
					,"appendPopularityInfo", "getTrackInfo", "getPopularity","appendScoreInfo"
					"getScore","getRecommendation","displayList"]
		# You have to have your own unique two values for API_KEY and API_SECRET
		# Obtain yours from http://www.last.fm/api/account for Last.fm
		API_KEY = "636d317dec99cfc2f19ce187a6d8c93d" # this is a sample key
		API_SECRET = "84a7ec870e3b95c88e841d5b6b72adf3"

		# In order to perform a write operation you need to authenticate yourself
		#username = "your_user_name"
		#password_hash = pylast.md5("your_password")

		#network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET, username = username, password_hash = password_hash)
		self.network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)
		pyechonest.config.ECHO_NEST_API_KEY="RJU1OKSCJG82R3IW7"

	def getSimilarArtists(self,name,limit):
		print "::getSimilarArtists (%s)"% (name)
		#limit = 10
		#name = "System of a Down"
		#artist = self.network.get_artist(name)
		#print "-------------:",artist
		artistSearchObj = self.network.search_for_artist(name)
		listOFArtists = artistSearchObj.get_next_page()
		#print "artist found:",len(listOFArtists)
		if(len(listOFArtists)==0):return None
		#print "artist::",listOFArtists[0]
		artist = listOFArtists[0]
		#for artist in listOFArtists:
		#	pprint(artist)
		#print "name:",name,", artist:",artist,", id:",artist.id
		similar = artist.get_similar(limit=limit)
		#pprint(similar)
		if limit is not None:
			similar = similar[:limit]
		return similar


	#not working yet. all tracks return null
	def getSimilarTracks(self,artist,title,limit):
		print "::getSimilarTracks (%s, %s)"% (artist, title)
		#limit = 10
		#name = "System of a Down"
		#track = self.network.get_track(artist,title)
		trackSearchObj = self.network.search_for_track(artist,title)
		listOfTracks = trackSearchObj.get_next_page()
		#print "artist found:",len(listOFArtists)
		if(len(listOfTracks)==0):return None
		track = listOfTracks[0]
		#print track
		similar = track.get_similar();
		'''
		print "--:",len(similar)
		for simItem in similar:
			pprint(simItem)
		'''
		if limit is not None:
			similar = similar[:limit]
		return similar


	def getAllTopTracks(self,artists, limit,weight_currentness, weight_similarness):
		print "::getAllTopTracks"
		TopList = list()
		for item in artists[:limit]:
			#if(len(TopList)>limit*10):return TopList
			#pprint (item)
			topTracks = pylast.Artist.get_top_tracks(item[0])
			#print "len---::",len(topTracks[0])
			for track in topTracks[:limit]:
				#print "Current Track -- > (%s, %s)"% (track[0].artist, track[0].title)
				#pprint(track[0].title)
				trackObj = {
								'artist':track[0].artist,
								'title':track[0].title,
								'similarity': item[1]
							}
				#pprint(trackObj['title'])
				trackObj = self.getTrackInfo(trackObj,weight_currentness, weight_similarness)
				if(trackObj!=None ):
					TopList.append(trackObj)

		#if limit is not None:
		#	TopList = TopList[:limit]
		return TopList

	def cleanData(self,tracks, limit,weight_currentness, weight_similarness):
		print "::cleanData"
		TopList = list()
		for item in tracks[:limit]:
			track = item[0]
			trackObj = {
								'artist':track.artist,
								'title':track.title,
								'similarity': item[1]
							}
			trackObj = self.getTrackInfo(trackObj,weight_currentness, weight_similarness)
			if(trackObj!=None):
				#pprint(trackObj)
				TopList.append(trackObj)
		return TopList	

	# not required anymore
	def appendPopularityInfo(self,listOfTracks,weight_currentness, weight_similarness):
		print "::appendPopularityInfo"
		for track in listOfTracks:
			track = self.getTrackInfo(track,weight_currentness, weight_similarness)
		return listOfTracks

	def getTrackInfo(self,track,weight_currentness, weight_similarness):
		if('artist' not in track):return None
		#if track==None : print "---------------"
		#print "::getTrackInfo (%s, %s)"% (track['artist'], track['title'])
		track['popularity'],track['familiarity'] = self.getPopularity(track['artist'],track['title'])
		track['score'],track['similar_component'],track['popular_component'] = self.getScore(track,weight_currentness, weight_similarness) 
		return track


	def getPopularity(self,artist_name,song_title):
		print "::getPopularity (%s, %s)"% (artist_name, song_title)
		track = pyechonest.song.search(artist=artist_name, title=song_title, results = 1)
		if(len(track)==0):
			return 0,0
		#pprint(track)
		Popularity = (track[0].song_hotttnesss+track[0].artist_hotttnesss)/2
		Familiarity = track[0].artist_familiarity 
		return Popularity,Familiarity

	def appendScoreInfo(self,listOfTracks):
		print "::appendScoreInfo"
		for track in listOfTracks:
			track['score'] = self.getScore(track) 
		return listOfTracks

	def getScore(self,track,weight_currentness, weight_similarness):
		#print "::getScore"
		Popularity = track['popularity']
		Familiarity = track['familiarity']
		Similarity = track['similarity']
		similar_component = ( Similarity * weight_similarness )
		popular_component = (Popularity*(1-weight_currentness) + Familiarity*weight_currentness)*(1-weight_similarness) 
		score = similar_component + popular_component  
		return score,similar_component,popular_component

	def getRecommendation(self, listOFArtists,artistLimit,trackLimit,weight_currentness, weight_similarness):
		print "::getRecommendation"
		TopList = list()
		similar = list()
		for artist in listOFArtists:
			sim = self.getSimilarArtists(artist['name'],artistLimit)
			if(sim!=None):
				similar.append(sim)

		for item in similar:
			topTracks = self.getAllTopTracks(item,trackLimit,weight_currentness, weight_similarness)
			if topTracks != None and len(topTracks)!=0 and 'score' in topTracks[0]:
				TopList.append(topTracks)
			#else:pprint(topTracks)

		for item in TopList:
			#print len(item)
			if len(item)==0:
				print "----found an empty one"
		return TopList


	def displayList2(self, TopList):
		print "::displayList"
		print "list len:",len(TopList)
		TopList = sorted(TopList, key=lambda track: track['score'], reverse=True)
		print "\tArtist - Title \t(Similarity, Popularity, Familiarity ,Score)"
		print "\t============================================================="
		for item in TopList:
			#print "len:",len(item)
			if len(item)!=0:
				print "\t%s - %s (%s, %s, %s) (%s : %s, %s)" % (item['artist'], item['title'], item['similarity'], item['popularity'], item['familiarity']
														,item['score'],item['similar_component'],item['popular_component'] )

	def displayList(self, TopList):
		print "::displayList"
		print "list len:",len(TopList)
		TopList = sorted(TopList, key=lambda track: track[0]['score'], reverse=True)
		print "\tArtist - Title \t(Similarity, Popularity, Familiarity ,Score)"
		print "\t============================================================="
		for track in TopList:
			#print "len:",len(item)
			item = track[0]
			if len(item)!=0:
				print "\t%s - %s (%s, %s, %s) (%s : %s, %s)" % (item['artist'], item['title'], item['similarity'], item['popularity'], item['familiarity']
														,item['score'],item['similar_component'],item['popular_component'] )

# Main
# ============

l = lastfm()
limit = 10
TopList = l.getSimilarTracks("Imagine Dragons", "My Fault",10)
l.cleanData(TopList,10,.5,.8)
#similar = l.getSimilarArtists("Snoop Dogg",limit)
#TopList = l.getAllTopTracks(similar,limit/3)
TopList = l.appendPopularityInfo(TopList,.5,.8)
l.displayList(TopList)
#TopList = appendScoreInfo(TopList)

