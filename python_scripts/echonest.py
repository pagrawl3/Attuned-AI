import pyechonest
from pyechonest import artist,song

pyechonest.config.ECHO_NEST_API_KEY="RJU1OKSCJG82R3IW7"

def getSimilarArtists(name,limit):
	print "::getSimilarArtists"
	curArtist = artist.Artist(name)
	artists = curArtist.get_similar(limit)
	print artists
	return artists

def getSimilarTracks(name,limit):
	print "::getSimilarTracks"
	return None

def getAllTopTracks(artists, limit):
	print "::getAllTopTracks"
	TopList =list()
	for curArtist in artists:
		#curArtist = artist.Artist(name)
		topTracks = curArtist.get_songs(results=limit)
		print topTracks
		TopList.append(topTracks)
	return TopList

limit = 10
artists = getSimilarArtists('Eminem',limit)
TopList = getAllTopTracks(artists,limit)
for curArtist in TopList:
	for curTrack in curArtist:
		print "\t%s \t%s" % (curTrack.title,curTrack.song_hotttnesss)
		#print "track:",curTrack.title

'''
results = song.search(artist='shakira', title='she wolf', buckets=['id:7digital', 'tracks'], limit=True, results=1)
print results
print "Artists similar to: %s:" % ('Eminem')
for similar_artist in artists: 
	print "\t%s" % (similar_artist)
'''