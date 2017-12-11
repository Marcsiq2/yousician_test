# -*- coding: utf-8 -*-
import argparse
import json
import urllib
import urllib2
import warnings
import numpy as np
from math import isnan
from pprint import pprint
from pymongo import MongoClient

PER_PAGE = 5

GET, POST = range(2)
hostname = None
port = None

client = MongoClient()
db = client.songs

songs = []
ids = []


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
    try:
    	response = urllib2.urlopen(req)
    	return json.loads(response.read())
    except urllib2.HTTPError as e:
    	print str(e.code) + " ERROR: " + e.read()
    


def add_songs():
	with open('songs.json') as data_file:
		for line in data_file:
			result = db.songs.insert_one(json.loads(line))
			songs.append(json.loads(line))
			ids.append(result.inserted_id)
			print 'Inserted song to MongoDB with ID: ' + str(result.inserted_id)

def del_songs():
	result = db.songs.delete_many({})
	print "Deleted " + str(result.deleted_count) + ' songs!'


def get_songs(page=None):
	if page:
		res = get_response('songs',{'page':page}, method=GET)
		if res:
			assert(res['result'] == songs[(page-1)*PER_PAGE:page*PER_PAGE])

	else:
		res = get_response('songs',{}, method=GET)
		if res:
			assert(res['result'] == songs)


def get_avg_difficulty(level=None):
	with warnings.catch_warnings():
		warnings.simplefilter("ignore", category=RuntimeWarning)
		if level:
			dif = [song['difficulty'] for song in songs if song['level']==level]
			avg = np.average(dif)
			res = get_response('songs/avg/difficulty', {'level':level})
		else:
			dif = [song['difficulty'] for song in songs]
			avg = np.average(dif)	
			res = get_response('songs/avg/difficulty', {})

		if res:
			if not (isnan(avg) and isnan(res['result'])):
				assert(res['result'] == avg)


def get_songs_search(message=None):
	if message:
		res = get_response('songs/search', {'message':message})
		s = [song for song in songs if (message.lower() in song['title'].lower() or message.lower() in song['artist'].lower())]
		if res:
			assert(res['result'] == s)
	else:
		res = get_response('songs/search', {})

def arating(id_num, rating=None):
	if not 'rating' in songs[id_num]:
		songs[id_num]['rating'] = []
	songs[id_num]['rating'].append(rating)
	res = add_rating(ids[id_num], rating)

def add_rating(song_id=None, rating=None):
	res = get_response('songs/rating', {'song_id':song_id, 'rating':rating}, method=POST)


def grating(id_num):
	resrat = dict()
	if 'rating' in songs[id_num]:
		rats = songs[id_num]['rating']
		resrat['highest'] = max(rats)
		resrat['lowest'] = min(rats)
		resrat['average'] = np.average(rats)
	res = get_rating(ids[id_num])
	if res:
		assert(res['result'] == resrat)

def get_rating(song_id=None):
	res = get_response(('songs/avg/rating/')+str(song_id), {})
	return res


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

	get_songs()
	get_avg_difficulty(3)

	del_songs()
	add_songs()

	get_songs()
	get_songs(page=2)
	get_songs(page=10)
	get_songs(page=-1) #400 response (not valid page)

	get_avg_difficulty()
	get_avg_difficulty(6)
	get_avg_difficulty(13)
	get_avg_difficulty(2)
	get_avg_difficulty(-3)
	get_avg_difficulty('s') #400 response (not valid level)

	get_songs_search('yousi')
	get_songs_search('IN')
	get_songs_search() #400 response (no message field)

	arating(3, 3)	
	arating(3, 5)
	arating(4, 5)
	add_rating('awaki', 3) #400 response (not valid id)
	add_rating(ids[3], 7) #400 response (not valid rating)

	grating(3)
	grating(5)
	get_rating('awaki') #400 response (not valid id)

	# del_songs()


	print "Success!"
