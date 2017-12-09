# -*- coding: utf-8 -*-
import argparse
import json
import urllib
import urllib2
from pprint import pprint
from pymongo import MongoClient


GET, POST = range(2)
hostname = None
port = None

client = MongoClient()
db = client.songs


def get_response(fct, data, method=GET):
    """
    Performs the query to the server and returns a string containing the response.
    """
    assert(method in (GET, POST))
    url = 'http://%s:%s/%s' % (hostname, port, fct)
    if method == GET:
        req = urllib2.Request('%s?%s' % (url, urllib.urlencode(data)))
    elif method == POST:
        req = urllib2.Request(url, urllib.urlencode(data))
    response = urllib2.urlopen(req)
    return response.read()


def add_songs():
	with open('songs.json') as data_file:
		for line in data_file:
			result = db.songs.insert_one(json.loads(line))
			print 'Inserted song to MongoDB with ID: ' + str(result.inserted_id)

def del_songs():
	result = db.songs.delete_many({})
	print "Deleted " + str(result.deleted_count) + ' songs!'


def get_songs():
	res = get_response('songs',{}, method=GET)
	print res

def get_avg_difficulty(level=None):
	if level:
		res = get_response('songs/avg/difficulty', {'level':level})
	else:
		res = get_response('songs/avg/difficulty', {})
	print res

def get_songs_search(message=None):
	res = get_response('songs/search', {'message':message})
	print res

def add_rating(song_id=None, rating=None):
	res = get_response('songs/rating', {'song_id':song_id, 'rating':rating}, method=POST)
	print res

def get_rating(song_id=None):
	res = get_response(('songs/avg/rating/')+song_id, {})
	print res


if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Yousician api test')
	
	parser.add_argument('-H', action="store", dest="hostname",
						default="localhost", type=str)
	parser.add_argument('-P', action="store", dest="port",
						default=5000, type=int)
	
	args = parser.parse_args()
	hostname = args.hostname
	port = args.port

	del_songs()
	add_songs()
	get_songs()
	get_avg_difficulty(6)
	get_avg_difficulty(13)
	get_avg_difficulty(2)
	get_avg_difficulty()
	get_songs_search('yousi')
	get_songs_search('IN')
	get_songs_search()
	add_rating('Awaki-Waki', 4)	
	add_rating('Awaki-Waki', 5)
	add_rating('Awaki-Waki', 1)	
	get_rating('Awaki-Waki')
	del_songs()

	print "Success!"
